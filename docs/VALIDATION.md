# Validation report — updated 5 November 2026

Command: `python -m pytest -q --junitxml=test-results.xml`

The merged UI/reporting baseline had **30 passing tests**. The Part 3 suite expands this to **59 tests**, with fresh execution against that integrated source during the 2–6 November testing window. See [current executed reports](reports/README.md) for actual results, duration, coverage, source hashes and pending manual acceptance cases. The original 29 October preparation run passed all 59 tests with 97.32% statement coverage and 91.94% branch coverage. Application behavior is unchanged by the Part 3 additions.

The 30-case baseline includes the six original analytics cases, 16 authentication/database/service cases (including five invalid-write scenarios), and eight Streamlit UI workflow cases. The Part 3 suite extends this to 25 pure unit, 20 integration and 14 AppTest system-workflow instances. Additions verify exact weights and thresholds, nonfinite input rejection, expired lockout recovery, backup restoration and rollback, legacy deduplication, failed sign-in, session expiry, live account revocation, attendance error presentation, Admin create/link forms and historical UI filtering.

The performance case executes 20 normal synthetic-data query/summary cycles within three seconds. This does not measure a browser page load or institutional-scale concurrency. Manual visual browser acceptance is delegated to the user at their request. No application server or browser preview was started for the UI revision. GitHub Actions results are separate evidence and must be checked on the PR.
