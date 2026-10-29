"""SQLite persistence with transactions, constraints and online backups."""
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
DB_PATH = os.environ.get('ACADEMIC_DB_PATH', str(Path(__file__).with_name('academic.db')))

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    try:
        with conn:
            yield conn
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS students (
          student_id INTEGER PRIMARY KEY, name TEXT NOT NULL, program TEXT,
          semester INTEGER CHECK(semester BETWEEN 1 AND 12));
        CREATE TABLE IF NOT EXISTS subjects (
          subject_id INTEGER PRIMARY KEY, code TEXT NOT NULL, name TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS academic_records (
          record_id INTEGER PRIMARY KEY AUTOINCREMENT,
          student_id INTEGER NOT NULL REFERENCES students(student_id),
          subject_id INTEGER NOT NULL REFERENCES subjects(subject_id), period TEXT NOT NULL,
          attendance_pct REAL NOT NULL CHECK(attendance_pct BETWEEN 0 AND 100),
          assignment_score REAL NOT NULL CHECK(assignment_score BETWEEN 0 AND 100),
          internal_score REAL NOT NULL CHECK(internal_score BETWEEN 0 AND 100),
          exam_score REAL NOT NULL CHECK(exam_score BETWEEN 0 AND 100));
        CREATE TABLE IF NOT EXISTS users (
          username TEXT PRIMARY KEY, password_hash TEXT NOT NULL,
          role TEXT NOT NULL CHECK(role IN ('Admin','Faculty','Student')),
          student_id INTEGER REFERENCES students(student_id), active INTEGER NOT NULL DEFAULT 1,
          CHECK(role != 'Student' OR student_id IS NOT NULL));
        CREATE TABLE IF NOT EXISTS audit_log (
          id INTEGER PRIMARY KEY, actor TEXT NOT NULL, action TEXT NOT NULL,
          detail TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')));
        CREATE TABLE IF NOT EXISTS login_attempts (
          username TEXT PRIMARY KEY, failures INTEGER NOT NULL, last_attempt REAL NOT NULL);
        ''')
        conn.execute('''DELETE FROM academic_records WHERE record_id NOT IN
          (SELECT MAX(record_id) FROM academic_records GROUP BY student_id,subject_id,period)''')
        conn.execute('CREATE UNIQUE INDEX IF NOT EXISTS record_key ON academic_records(student_id,subject_id,period)')

def backup_database(destination):
    target = Path(destination).resolve()
    if target == Path(DB_PATH).resolve():
        raise ValueError('Backup destination must differ from database')
    target.parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as source:
        backup = sqlite3.connect(target)
        try:
            source.backup(backup)
        finally:
            backup.close()
