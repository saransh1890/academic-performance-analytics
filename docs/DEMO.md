# Sprint demonstration scripts

Use synthetic data. Keep generated passwords off-screen. Record actual working interactions and save the outcome videos in the repository. State actual recording dates. These scripts are not evidence that the videos exist.

## Sprint 1 outcome - one minute

- 0:00-0:10: introduce Academic Performance Analytics and sign in as Faculty, with password entry omitted.
- 0:10-0:35: record attendance and assessment marks for a synthetic student; save the record.
- 0:35-0:55: show that Student's own dashboard, calculated score, attendance and assessment history.
- 0:55-1:00: summarize the working core and authenticated access.

## Sprint 2 outcome - two minutes

- 0:00-0:30: class summary, trends and Faculty-only intervention filter with explained reasons.
- 0:30-0:55: subject/period filters and class or individual CSV report download.
- 0:55-1:25: Admin student, subject and account management; keep credentials private.
- 1:25-1:45: audit entry from a record edit and local backup creation.
- 1:45-2:00: show actual passing tests/reports and explain the service API replacing the original REST sketch.

## Individual contribution explanation

Saransh: foundation/authentication/accounts (PR 13). Maneesh: academic persistence/validation/audit (PR 14). Suhas: analytics/trends/intervention/reporting (PR 15). Akash: UI/forms/styling/integration/CI/document integration (PR 16). Suhas also submitted testing reports in PR 17. Each member should show their actual assigned issue, estimate, PR and relevant code during the viva.

## Final acceptance

Manually check all three roles, Student peer exclusion, rejected attendance, edit without duplicates, empty subject state, CSV opening and backup recovery readiness. Record browser load timing, tester/date/results and owner approval. Freeze only after remaining defects and acceptance conditions are addressed.
