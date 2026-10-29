# Validation report — 29 October 2026

Command: `python -m pytest -q --junitxml=test-results.xml`

Latest result after the UI and reporting revision: **30 passed in 40.80 seconds** on Windows, Python 3.11.9, with the dependency versions in requirements-lock.txt. The previous implementation baseline had 24 passing tests.

Coverage includes the six original analytics cases, 16 authentication/database/service cases (including five invalid-write scenarios), and eight Streamlit UI workflow cases. UI tests exercise student sign-in and logout with peer-data exclusion, faculty academic entry and report navigation, the administrator workspace, Faculty-only intervention filter visibility and behavior, Student support reasons, existing-record prefilling and subject empty states. Integration cases cover record uniqueness, audit atomicity, foreign keys, numeric period ordering, multi-subject aggregation, account revocation, idempotent seeding, backup consistency, CSV formula escaping, individual reports and intervention-filtered report contents.

The performance case executes 20 normal synthetic-data query/summary cycles within three seconds. This does not measure a browser page load or institutional-scale concurrency. Manual visual browser acceptance is delegated to the user at their request. No application server or browser preview was started for the UI revision. GitHub Actions results are separate evidence and must be checked on the PR.
