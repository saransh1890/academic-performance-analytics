import sqlite3

DB_PATH = "academic.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            program TEXT,
            semester INTEGER
        );
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY,
            code TEXT NOT NULL,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS academic_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            period TEXT NOT NULL,
            attendance_pct REAL NOT NULL,
            assignment_score REAL NOT NULL,
            internal_score REAL NOT NULL,
            exam_score REAL NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
        );
        """)
