# Academic Performance Analytics

A working Streamlit web application for the SE mini-project. It includes authenticated Student, Faculty and Admin workspaces, academic data entry, period and subject filters, trend charts, intervention flags, CSV reports, audit history and database backups.

## Start on Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python seed_data.py
.\.venv\Scripts\python -m streamlit run app.py
```

Open http://localhost:8501. The seed command prints randomly generated passwords for `admin`, `faculty`, and `student1` through `student5` only when creating those accounts. Save the passwords locally. Re-running seed preserves accounts and records. Admin can reset another account's password from Administration. For a fresh synthetic demonstration, use a new `ACADEMIC_DB_PATH`; do not delete real data to reset credentials.

On macOS/Linux use `.venv/bin/python` instead. Python 3.11 is the reference environment. `requirements-lock.txt` records the validated local dependency versions; `requirements.txt` defines the direct dependencies.

## Using the UI

- Student: see personal performance, attendance, trend, assessment period, own support status and history. Class controls and the intervention filter are absent.
- Faculty: view class analytics, filter by subject/period, optionally show only students who need intervention, save attendance and marks, and export a class or individual-student report.
- Admin: view overall analytics and reports, maintain academic data, students, subjects and accounts, inspect the latest 200 audit entries and create local database backups. The intervention-only checkbox is Faculty-only.
- Academic data: choose a student, subject and P1/P2/etc. Existing marks and attendance percentage preload for editing. Enter attendance as class counts or a percentage and assessment values out of 100. Saving the same student/subject/period updates its record.
- Reports: choose Class summary or a named student under Report scope. CSV output follows the subject, period, report scope and active Faculty intervention filter. An empty selection exports headers with no rows.
- Administration forms: use an existing ID to update a student or subject. Account save creates an account or resets its password and permissions. Sign out using the sidebar.

## Rules

Score = 40% exam + 25% assignment + 20% attendance + 15% internal. Subject indicators are equally weighted within each period. Trend compares that period to the immediately preceding available period (P2 before P10). A drop/rise of at least 10 points means Declining/Improving. Intervention: score < 50 OR attendance < 75% OR declining. No records means an empty state, not a zero score. Historical filters never use future periods.

These criteria are project assumptions, not institutional policy. All demonstration records are synthetic. Faculty access is institution-wide because the SRS does not define faculty/course assignments.

## Tests and delivery

```powershell
.\.venv\Scripts\python -m pytest -q --junitxml=test-results.xml
```

GitHub Actions runs the test suite on pushes and pull requests. See [delivery status](docs/DELIVERY.md), [requirements and design](docs/IMPLEMENTATION.md), [UI changes and requirements review](docs/UI_AND_REQUIREMENTS_REVIEW.md), [backlog](docs/BACKLOG.md), and [demo script](docs/DEMO.md). Original SRS, SAD and Test Plan DOCX submissions are preserved; implementation details and deviations are in these companion documents.

## Data and recovery

SQLite defaults to `academic.db` next to the source. Set `ACADEMIC_DB_PATH` before startup to use a different file. Seed is explicit; the app never silently inserts sample data. Passwords use salted PBKDF2-SHA256, access is checked in services, accounts are revalidated on each interaction, sign-in is throttled, sessions expire after 30 minutes of inactivity, and SQL values are parameterized. Deploy behind HTTPS with restricted filesystem access. This is a single-instance course prototype.

Before releases or data migrations, create a backup from Administration. Stop the server before restoring: retain a copy of the current database, copy the selected backup to the configured database path, then restart and verify logins and record counts. Backups contain private data and must stay outside Git. Initialization upgrades the original schema and deduplicates old seed records, retaining the highest record ID per student/subject/period.

## Team

| Member | SRN |
|---|---|
| Saransh Mittal | PES1UG24AM254 |
| TB Akash | PES1UG24AM299 |
| Sanapala Maneesh | PES1UG24AM247 |
| Suhas MK | PES1UG24AM290 |
