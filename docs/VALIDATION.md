# Validation report — 29 October 2026

Command: `python -m pytest -q --junitxml=test-results.xml`

Result: **24 passed in 31.79 seconds** on Windows, Python 3.11.9, with the dependency versions in requirements-lock.txt.

Coverage includes the six original analytics cases, 15 authentication/database/service cases (including five invalid-write scenarios), and three Streamlit UI workflow cases. UI tests exercise student sign-in and logout with peer-data exclusion, faculty academic entry and report navigation, and the administrator workspace. Integration cases cover record uniqueness, audit atomicity, foreign keys, numeric period ordering, multi-subject aggregation, account revocation, idempotent seeding, backup consistency and CSV formula escaping.

The performance case executes 20 normal synthetic-data query/summary cycles within three seconds. This does not measure a browser page load or institutional-scale concurrency. Manual visual browser acceptance is delegated to the user at their request. GitHub Actions results are separate evidence and must be checked on the PR.
