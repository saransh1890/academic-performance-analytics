# Demonstration scripts

Use only the synthetic database. Run seed locally and keep generated passwords off-screen. Set browser zoom so charts and tables are readable. Record actual application interaction and save MP4 files in docs/demos/ (or attach as GitHub release assets if too large). These scripts are not recordings.

## Sprint 1 outcome — 2 minutes

- 0:00–0:20: title and scope; sign in as faculty with credential entry omitted from recording.
- 0:20–0:50: show class metrics and students flagged for attendance/performance.
- 0:50–1:20: Academic data, add P3 for a synthetic student; demonstrate attended/conducted classes and valid marks.
- 1:20–1:45: sign out, sign in as that student; show own record and trend chart.
- 1:45–2:00: explain authentication and permissions. State honestly this demonstrates the first-sprint feature set recorded on the actual date.

## Sprint 2 outcome — 2 minutes

- 0:00–0:30: faculty dashboard, subject and period filters, intervention explanations.
- 0:30–1:00: demonstrate class trend and download the CSV report.
- 1:00–1:25: admin profiles, subjects and accounts; show audit entry from the academic edit.
- 1:25–1:45: create a local backup and show passing tests/PR checks without exposing private files or passwords.
- 1:45–2:00: explain the Streamlit service architecture deviation from the illustrative REST sketch, and identify any open team evidence.

## Final manual checks

Sign in under all three roles; verify tables and charts render on desktop; confirm student cannot select another student; submit invalid class counts and confirm error; update an existing record without duplicate rows; select a subject with no records and confirm empty state; export and open CSV; create a backup; sign out; ensure private data is ignored by Git.
