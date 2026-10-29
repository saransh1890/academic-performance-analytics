"""Idempotently add synthetic examples; existing user credentials are preserved."""
import secrets
from database import init_db, get_conn
from services import password_hash


def seed():
    init_db()
    students = [(1,'Aarav','CSE',5),(2,'Diya','CSE',5),(3,'Rohan','CSE',5),
                (4,'Meera','CSE',5),(5,'Kabir','CSE',5)]
    records = [(1,1,'P1',90,82,80,86),(1,1,'P2',88,78,75,76),
               (2,1,'P1',80,75,76,78),(2,1,'P2',81,77,78,80),
               (3,1,'P1',78,70,70,72),(3,1,'P2',70,62,60,55),
               (4,1,'P1',68,65,64,60),(4,1,'P2',66,61,55,48),
               (5,1,'P1',92,88,89,90),(5,1,'P2',93,90,92,94)]
    credentials = {}
    with get_conn() as conn:
        conn.executemany('INSERT OR IGNORE INTO students VALUES(?,?,?,?)', students)
        conn.execute("INSERT OR IGNORE INTO subjects VALUES(1,'SE101','Software Engineering')")
        conn.execute("INSERT OR IGNORE INTO subjects VALUES(2,'DB101','Database Systems')")
        conn.executemany('''INSERT OR IGNORE INTO academic_records
          (student_id,subject_id,period,attendance_pct,assignment_score,internal_score,exam_score)
          VALUES(?,?,?,?,?,?,?)''', records)
        for username, role, sid in [('admin','Admin',None),('faculty','Faculty',None)] + [(f'student{i}','Student',i) for i in range(1,6)]:
            if not conn.execute('SELECT 1 FROM users WHERE username=?', (username,)).fetchone():
                password = secrets.token_urlsafe(15)
                conn.execute('INSERT INTO users VALUES(?,?,?,?,1)', (username,password_hash(password),role,sid))
                credentials[username] = password
    return credentials

if __name__ == '__main__':
    credentials = seed()
    print('Synthetic data ready. Existing records and credentials preserved.')
    for username, password in credentials.items():
        print(f'{username}: {password}')
    if credentials:
        print('Save these generated local passwords securely; they are shown only on account creation.')
