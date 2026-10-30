"""Authorization, validated writes, reporting and analytics application layer."""
import hashlib
import hmac
import math
import os
import re
import time
from dataclasses import dataclass
import pandas as pd
from analytics import performance_score, trend_status, intervention_status
from database import get_conn

@dataclass(frozen=True)
class Principal:
    username: str


def password_hash(password):
    if len(password) < 10:
        raise ValueError('Password must contain at least 10 characters')
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 260000).hex()
    return f'pbkdf2_sha256$260000${salt}${digest}'


def verify_password(password, encoded):
    try:
        _, iterations, salt, digest = encoded.split('$')
        actual = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), int(iterations)).hex()
        return hmac.compare_digest(actual, digest)
    except (ValueError, TypeError):
        return False


def authenticate(username, password):
    with get_conn() as conn:
        attempt = conn.execute('SELECT * FROM login_attempts WHERE username=?', (username,)).fetchone()
        if attempt and attempt['failures'] >= 5 and time.time() - attempt['last_attempt'] < 300:
            return None
        user = conn.execute('SELECT * FROM users WHERE username=? AND active=1', (username,)).fetchone()
        if user and verify_password(password, user['password_hash']):
            conn.execute('DELETE FROM login_attempts WHERE username=?', (username,))
            return Principal(username)
        count = attempt['failures'] if attempt and time.time() - attempt['last_attempt'] < 300 else 0
        conn.execute('INSERT OR REPLACE INTO login_attempts VALUES(?,?,?)', (username, count + 1, time.time()))
    return None


def authorize(principal, roles=('Admin', 'Faculty', 'Student')):
    if not isinstance(principal, Principal):
        raise PermissionError('Please sign in')
    with get_conn() as conn:
        row = conn.execute('SELECT username,role,student_id FROM users WHERE username=? AND active=1', (principal.username,)).fetchone()
    if row is None or row['role'] not in roles:
        raise PermissionError('Your account cannot perform this action')
    return dict(row)


def audit(conn, user, action, detail):
    conn.execute('INSERT INTO audit_log(actor,action,detail) VALUES(?,?,?)', (user['username'], action, detail))


def text(value, label):
    value = str(value).strip()
    if not value or len(value) > 120:
        raise ValueError(f'{label} must contain 1 to 120 characters')
    return value


def save_student(principal, student_id, name, program, semester):
    user = authorize(principal, ('Admin',))
    if int(student_id) <= 0 or not 1 <= int(semester) <= 12:
        raise ValueError('Use a positive student ID and semester between 1 and 12')
    with get_conn() as conn:
        conn.execute('''INSERT INTO students VALUES(?,?,?,?) ON CONFLICT(student_id)
          DO UPDATE SET name=excluded.name,program=excluded.program,semester=excluded.semester''',
          (int(student_id), text(name, 'Name'), text(program, 'Program'), int(semester)))
        audit(conn, user, 'student.save', str(student_id))


def save_subject(principal, subject_id, code, name):
    user = authorize(principal, ('Admin',))
    if int(subject_id) <= 0:
        raise ValueError('Use a positive subject ID')
    with get_conn() as conn:
        conn.execute('''INSERT INTO subjects VALUES(?,?,?) ON CONFLICT(subject_id)
          DO UPDATE SET code=excluded.code,name=excluded.name''',
          (int(subject_id), text(code, 'Code'), text(name, 'Subject name')))
        audit(conn, user, 'subject.save', str(subject_id))


def save_user(principal, username, password, role, student_id=None, active=True):
    user = authorize(principal, ('Admin',))
    username = text(username, 'Username')
    if role not in ('Admin', 'Faculty', 'Student') or (role == 'Student' and student_id is None):
        raise ValueError('Select a valid role and link student accounts to a student')
    if username == user['username'] and (not active or role != 'Admin'):
        raise ValueError('You cannot disable or demote your own administrator account')
    encoded = password_hash(password)
    with get_conn() as conn:
        conn.execute('''INSERT INTO users VALUES(?,?,?,?,?) ON CONFLICT(username) DO UPDATE SET
          password_hash=excluded.password_hash,role=excluded.role,student_id=excluded.student_id,active=excluded.active''',
          (username, encoded, role, student_id if role == 'Student' else None, int(active)))
        audit(conn, user, 'user.save', username)


def save_record(principal, student_id, subject_id, period, attended, total, assignment, internal, exam):
    user = authorize(principal, ('Admin', 'Faculty'))
    period = text(period, 'Period').upper()
    if not re.fullmatch(r'P[1-9][0-9]{0,3}', period):
        raise ValueError('Period must be P1, P2, ... P9999')
    if not math.isfinite(total) or not math.isfinite(attended) or total <= 0 or attended < 0 or attended > total:
        raise ValueError('Attendance requires 0 <= attended <= total and total > 0')
    attendance = round(attended / total * 100, 2)
    performance_score(exam, assignment, attendance, internal)
    with get_conn() as conn:
        before = conn.execute('SELECT * FROM academic_records WHERE student_id=? AND subject_id=? AND period=?', (student_id, subject_id, period)).fetchone()
        conn.execute('''INSERT INTO academic_records(student_id,subject_id,period,attendance_pct,assignment_score,internal_score,exam_score)
          VALUES(?,?,?,?,?,?,?) ON CONFLICT(student_id,subject_id,period) DO UPDATE SET
          attendance_pct=excluded.attendance_pct,assignment_score=excluded.assignment_score,
          internal_score=excluded.internal_score,exam_score=excluded.exam_score''',
          (student_id, subject_id, period, attendance, assignment, internal, exam))
        audit(conn, user, 'record.update' if before else 'record.create',
              f'student={student_id};subject={subject_id};period={period};before={dict(before) if before else None};after={(attendance, assignment, internal, exam)}')


def catalog(principal):
    user = authorize(principal)
    with get_conn() as conn:
        students = pd.read_sql_query('SELECT * FROM students' + (' WHERE student_id=?' if user['role'] == 'Student' else '') + ' ORDER BY student_id', conn,
                                     params=(user['student_id'],) if user['role'] == 'Student' else ())
        subjects = pd.read_sql_query('SELECT * FROM subjects ORDER BY subject_id', conn)
    return students, subjects


def records_for(principal, subject_id=None, period=None):
    user = authorize(principal)
    clauses, params = [], []
    if user['role'] == 'Student':
        clauses.append('r.student_id=?')
        params.append(user['student_id'])
    if subject_id is not None:
        clauses.append('r.subject_id=?')
        params.append(int(subject_id))
    if period:
        clauses.append('r.period=?')
        params.append(period)
    query = '''SELECT r.*,s.name,s.program,s.semester,t.code,t.name AS subject
      FROM academic_records r JOIN students s USING(student_id) JOIN subjects t USING(subject_id)'''
    if clauses:
        query += ' WHERE ' + ' AND '.join(clauses)
    with get_conn() as conn:
        return pd.read_sql_query(query, conn, params=params)


def period_key(period):
    parts = re.split(r'(\d+)', str(period))
    return tuple((1, int(p)) if p.isdigit() else (0, p) for p in parts)


def summarize(records, period=None):
    columns = ['Student ID', 'Student', 'Program', 'Period', 'Score', 'Attendance', 'Trend', 'Status', 'Reasons']
    rows = []
    for sid, data in records.groupby('student_id'):
        means = data.groupby('period')[['exam_score', 'assignment_score', 'attendance_pct', 'internal_score']].mean()
        periods = sorted(means.index, key=period_key)
        if period and period not in periods:
            continue
        latest_period = period or periods[-1]
        index = periods.index(latest_period)
        latest = means.loc[latest_period]
        score = performance_score(*map(float, latest))
        previous = performance_score(*map(float, means.loc[periods[index - 1]])) if index else None
        trend = trend_status(previous, score)
        status, reasons = intervention_status(score, float(latest.attendance_pct), trend)
        rows.append([int(sid), data.iloc[0]['name'], data.iloc[0]['program'], latest_period, score,
                     round(float(latest.attendance_pct), 2), trend, status, ', '.join(reasons)])
    return pd.DataFrame(rows, columns=columns)


def export_report(principal, subject_id=None, period=None, student_id=None, risk_only=False):
    authorize(principal, ('Admin', 'Faculty'))
    frame = summarize(records_for(principal, subject_id), period)
    if student_id is not None:
        frame = frame[frame['Student ID'] == int(student_id)]
    if risk_only:
        frame = frame[frame.Status == 'Needs Intervention']
    # Prevent spreadsheet applications interpreting names as formulas.
    for column in ('Student', 'Program', 'Period', 'Trend', 'Status', 'Reasons'):
        frame[column] = frame[column].map(lambda v: "'" + v if isinstance(v, str) and v.startswith(('=', '+', '-', '@', '\t', '\r', '\n')) else v)
    return frame.to_csv(index=False).encode('utf-8-sig')


def administration(principal):
    authorize(principal, ('Admin',))
    with get_conn() as conn:
        return (pd.read_sql_query('SELECT username,role,student_id,active FROM users', conn),
                pd.read_sql_query('SELECT * FROM audit_log ORDER BY id DESC LIMIT 200', conn))
