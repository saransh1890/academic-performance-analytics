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














