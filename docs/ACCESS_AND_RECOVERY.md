# Access and recovery acceptance

Use a freshly seeded synthetic database. Record the tester, date, source commit and observed result for each scenario.

| Scenario | Expected result |
| --- | --- |
| Five incorrect Faculty passwords followed by the correct password | Sign-in stays blocked for the lockout window. |
| Admin resets the locked Faculty account | The replacement password signs in. The old password fails. |
| Admin deactivates a signed-in Student | That Student is returned to sign-in on the next action. |
| Admin creates a backup after a record save | The backup contains the saved record and passes the SQLite integrity check below. |

Check the backup with Python without switching the application database. Substitute the local backup path.

```powershell
.\.venv\Scripts\python.exe -c "import sqlite3,sys,pathlib; p=pathlib.Path(sys.argv[1]).resolve(); c=sqlite3.connect(p.as_uri()+'?mode=ro', uri=True); print(c.execute('PRAGMA integrity_check').fetchone()[0]); print(c.execute('SELECT count(*) FROM academic_records').fetchone()[0])" 'C:\path\to\backup.db'
```

For a recovery rehearsal, make a copy of the backup and start the app with `ACADEMIC_DB_PATH` pointing to that copy. Verify sign-in and record counts against the snapshot. Keep backup files and generated credentials private.
