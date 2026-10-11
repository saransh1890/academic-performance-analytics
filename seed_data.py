from database import init_db, get_conn

init_db()
students = [
    (1, "Aarav", "CSE", 5), (2, "Diya", "CSE", 5),
    (3, "Rohan", "CSE", 5), (4, "Meera", "CSE", 5),
    (5, "Kabir", "CSE", 5)
]
subjects = [(1, "SE101", "Software Engineering")]
records = [
    (1,1,"P1",90,82,80,86),(1,1,"P2",88,78,75,76),
    (2,1,"P1",80,75,76,78),(2,1,"P2",81,77,78,80),
    (3,1,"P1",78,70,70,72),(3,1,"P2",70,62,60,55),
    (4,1,"P1",68,65,64,60),(4,1,"P2",66,61,55,48),
    (5,1,"P1",92,88,89,90),(5,1,"P2",93,90,92,94)
]
with get_conn() as conn:
    conn.executemany("INSERT OR IGNORE INTO students VALUES (?,?,?,?)", students)
    conn.executemany("INSERT OR IGNORE INTO subjects VALUES (?,?,?)", subjects)
    conn.executemany("""INSERT INTO academic_records
        (student_id,subject_id,period,attendance_pct,assignment_score,internal_score,exam_score)
        VALUES (?,?,?,?,?,?,?)""", records)
print("Synthetic demo data inserted.")
