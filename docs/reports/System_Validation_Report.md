# System Validation Report

Executed evidence generated 2026-11-05T08:50:24+05:30. Source base: `bf35375`; the run manifest records any local source changes and SHA-256 hashes of the measured files. This reporting command does not push, start a server or open a browser.

Python 3.11.9 on Windows; pytest 9.2.0, coverage 7.17.0, streamlit 1.66.1, pandas 3.1.0, plotly 7.1.0. Synthetic databases are isolated in temporary test directories.

**59/59 tests passed**, comprising 25 unit, 20 integration and 14 automated system-workflow cases. Total suite duration: 62.95 seconds.

## Automated validation conclusion

The automated application workflows and integration checks passed for this source snapshot. Overall acceptance is **PENDING MANUAL VALIDATION**, not an unconditional release approval. AppTest exercises server-side Streamlit widgets and state; it does not render browser pixels, measure network latency or establish live availability.

| Automated system case | Expected behavior | Result |
|---|---|---|
| TC-007: Student dashboard and logout | Own metrics and history appear; peer data/class controls are absent; logout returns to sign-in | PASS |
| TC-008: Faculty record-to-report workflow | Record saves successfully; report page opens and class metrics remain available | PASS |
| TC-009: Administrator workspace | Student, subject, account and audit/backup tabs render | PASS |
| TC-010: Faculty intervention filter | Filter returns two flagged students; clearing restores five; report scope is available | PASS |
| TC-011: Admin filter visibility | Faculty-only checkbox is absent from Admin dashboard and reports | PASS |
| TC-012: Student support feedback | Rohan sees own low-attendance and declining reasons without class filter | PASS |
| TC-013: Existing academic record editing | Existing 90/82/80/86 indicators preload and save successfully | PASS |
| TC-014: Empty student subject view | Subject without records shows a message without metrics or class filter | PASS |
| TC-015: Failed sign-in workflow | Error appears; protected metrics remain absent | PASS |
| TC-016: Session inactivity expiry | Session older than 1800 seconds returns to sign-in | PASS |
| TC-017: Active session account revocation | Deactivated student session loses dashboard access on next interaction | PASS |
| TC-018: Attendance error message | Attending 5 of 4 classes shows an understandable validation error | PASS |
| TC-019: Admin create and account-link workflow | Student and subject are created; linked account authenticates and has no peer records | PASS |
| TC-020: Historical dashboard filter | Selecting P1 shows P1 summaries/history without future periods | PASS |

## Supporting integration checks

Validated authorization and revoked access; percentage calculation and unique upserts; atomic audits and rejected inputs; foreign keys; period and subject filtering; individual and risk-only exports; formula escaping; seed idempotency; backup consistency and recovery; migration of old duplicate seed rows; and transaction rollback.

The normal-load case asserts that 20 synthetic query-and-summary cycles finish within three seconds. This is a local service test, not proof of the SRS browser dashboard load target.

## Manual acceptance still required

- **MAN-01 Desktop visual acceptance (NF004) - PENDING.** Use Student, Faculty and Admin at 1366x768 and 1920x1080; inspect sign-in, forms, tables, charts and sidebar. Expected: All content readable; no clipping or overlap; controls match role.
- **MAN-02 Browser load target (NF001) - PENDING.** Start the final app and time warm dashboard loads on the target machine; record data volume and timings. Expected: Dashboard loads within 3 seconds under normal project-test load.
- **MAN-03 Demonstration readiness (NF002) - PENDING.** Start from documented commands on the demo machine and sign in under all roles. Expected: App remains usable during the planned demonstration.
- **MAN-04 Downloaded report acceptance (F014) - PENDING.** Download a class and individual report; open in the intended spreadsheet application. Expected: Rows, encoding, filters and indicator labels match the chosen scope.
- **MAN-05 Release backup sign-off (NF005) - PENDING.** Create a backup before release and confirm the selected snapshot and documented recovery location. Expected: Backup exists and the team can identify the recovery procedure.
- **MAN-06 Final acceptance (Course) - PENDING.** Team records tester, date, observed result and owner decision after manual checks. Expected: Owner signs off only after pending checks and defects are resolved.

## Defect and acceptance status

No automated failures occurred in this run. This is not a claim of zero undiscovered defects. No human visual results, owner approval, demo recordings, final freeze or GitHub upload are fabricated. The optional Sprint 3 is needed only if actual development spillover occurs during 2-6 November.

Evidence: [system JUnit](evidence/system-junit.xml), [full JUnit](evidence/junit.xml), [test cases](Test_Case_Document.md), [run manifest](evidence/run-manifest.json).
