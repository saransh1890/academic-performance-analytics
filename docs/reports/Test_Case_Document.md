# Updated Test Case Document

Executed evidence generated 2026-11-05T08:50:24+05:30. Source base: `bf35375`; the run manifest records any local source changes and SHA-256 hashes of the measured files. This reporting command does not push, start a server or open a browser.

This document updates the original Test_Plan.docx with sprint changes and recorded outcomes. Requirements use the AAS- prefix from SRS.docx.

**59/59 tests passed**, comprising 25 unit, 20 integration and 14 automated system-workflow cases. Total suite duration: 62.95 seconds.

Python 3.11.9 on Windows; pytest 9.2.0, coverage 7.17.0, streamlit 1.66.1, pandas 3.1.0, plotly 7.1.0. Synthetic databases are isolated in temporary test directories.

## Preconditions and execution

Install requirements-test.txt and run `python scripts/run_part3_checks.py`. Tests initialize only synthetic temporary databases. Automated system cases execute Streamlit AppTest, not a browser. Expected outcomes below are asserted in the linked test implementations; each parameterized instance is recorded separately. Raw node names and timings are in evidence/run-manifest.json and evidence/junit.xml.

## Executed test cases

| ID | Type | Requirement | Scenario and test instance | Expected outcome | Actual result |
|---|---|---|---|---|---|
| TC-001 | Unit | F008,NF006 | Equal assessment indicators<br>`test_performance_score` | All indicators at 80 produce score 80 | PASS: all assertions passed |
| TC-002 | Unit | F011/012 | Declining score<br>`test_declining_trend` | 75 to 64 is Declining | PASS: all assertions passed |
| TC-003 | Unit | F011 | Improving score<br>`test_improving_trend` | 60 to 72 is Improving | PASS: all assertions passed |
| TC-004 | Unit | F011 | Stable score<br>`test_stable_trend` | 70 to 75 is Stable | PASS: all assertions passed |
| TC-005 | Unit | F013 | Low attendance<br>`test_low_attendance_triggers_intervention` | 60 percent attendance triggers a low-attendance reason | PASS: all assertions passed |
| TC-006 | Unit | SR006 | Out-of-range score<br>`test_invalid_score_inputs_rejected` | Score above 100 is rejected | PASS: all assertions passed |
| TC-007 | System | F001/009/015 | Student dashboard and logout<br>`test_login_and_student_dashboard` | Own metrics and history appear; peer data/class controls are absent; logout returns to sign-in | PASS: all assertions passed |
| TC-008 | System | F004/006/007/010/014 | Faculty record-to-report workflow<br>`test_faculty_record_flow` | Record saves successfully; report page opens and class metrics remain available | PASS: all assertions passed |
| TC-009 | System | F002/003,SR002 | Administrator workspace<br>`test_admin_screen` | Student, subject, account and audit/backup tabs render | PASS: all assertions passed |
| TC-010 | System | F010/013/014 | Faculty intervention filter<br>`test_faculty_intervention_filter_and_report_scope` | Filter returns two flagged students; clearing restores five; report scope is available | PASS: all assertions passed |
| TC-011 | System | SR002 | Admin filter visibility<br>`test_admin_has_no_intervention_filter` | Faculty-only checkbox is absent from Admin dashboard and reports | PASS: all assertions passed |
| TC-012 | System | F009/013/015 | Student support feedback<br>`test_student_sees_own_support_reasons` | Rohan sees own low-attendance and declining reasons without class filter | PASS: all assertions passed |
| TC-013 | System | F004/006/007 | Existing academic record editing<br>`test_existing_marks_are_prefilled` | Existing 90/82/80/86 indicators preload and save successfully | PASS: all assertions passed |
| TC-014 | System | F009/016 | Empty student subject view<br>`test_subject_with_no_records_shows_empty_state` | Subject without records shows a message without metrics or class filter | PASS: all assertions passed |
| TC-015 | System | F001,SR001 | Failed sign-in workflow<br>`test_failed_signin_stays_on_login` | Error appears; protected metrics remain absent | PASS: all assertions passed |
| TC-016 | System | SR001/002 | Session inactivity expiry<br>`test_expired_session_returns_to_login` | Session older than 1800 seconds returns to sign-in | PASS: all assertions passed |
| TC-017 | System | SR002/003 | Active session account revocation<br>`test_revoked_account_returns_to_login` | Deactivated student session loses dashboard access on next interaction | PASS: all assertions passed |
| TC-018 | System | F004/005,SR006 | Attendance error message<br>`test_invalid_attendance_shows_error` | Attending 5 of 4 classes shows an understandable validation error | PASS: all assertions passed |
| TC-019 | System | F002/003,SR002 | Admin create and account-link workflow<br>`test_admin_management_forms_save` | Student and subject are created; linked account authenticates and has no peer records | PASS: all assertions passed |
| TC-020 | System | F011/016 | Historical dashboard filter<br>`test_historical_filter_excludes_future_records` | Selecting P1 shows P1 summaries/history without future periods | PASS: all assertions passed |
| TC-021 | Unit | F008,NF006 | Independent formula weights<br>`test_independent_weights_and_boundaries[inputs0-40]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS: all assertions passed |
| TC-022 | Unit | F008,NF006 | Independent formula weights<br>`test_independent_weights_and_boundaries[inputs1-25]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS: all assertions passed |
| TC-023 | Unit | F008,NF006 | Independent formula weights<br>`test_independent_weights_and_boundaries[inputs2-20]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS: all assertions passed |
| TC-024 | Unit | F008,NF006 | Independent formula weights<br>`test_independent_weights_and_boundaries[inputs3-15]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS: all assertions passed |
| TC-025 | Unit | F008,NF006 | Independent formula weights<br>`test_independent_weights_and_boundaries[inputs4-0]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS: all assertions passed |
| TC-026 | Unit | F008,NF006 | Independent formula weights<br>`test_independent_weights_and_boundaries[inputs5-100]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS: all assertions passed |
| TC-027 | Unit | SR006 | Numeric validation boundaries<br>`test_nonfinite_and_invalid_scores[-0.01]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS: all assertions passed |
| TC-028 | Unit | SR006 | Numeric validation boundaries<br>`test_nonfinite_and_invalid_scores[100.01]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS: all assertions passed |
| TC-029 | Unit | SR006 | Numeric validation boundaries<br>`test_nonfinite_and_invalid_scores[inf]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS: all assertions passed |
| TC-030 | Unit | SR006 | Numeric validation boundaries<br>`test_nonfinite_and_invalid_scores[-inf]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS: all assertions passed |
| TC-031 | Unit | SR006 | Numeric validation boundaries<br>`test_nonfinite_and_invalid_scores[nan]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS: all assertions passed |
| TC-032 | Unit | SR006 | Numeric validation boundaries<br>`test_nonfinite_and_invalid_scores[80]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS: all assertions passed |
| TC-033 | Unit | SR006 | Numeric validation boundaries<br>`test_nonfinite_and_invalid_scores[None]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS: all assertions passed |
| TC-034 | Unit | F011/012 | Exact trend boundaries<br>`test_exact_trend_thresholds[None-80-No Previous Data]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS: all assertions passed |
| TC-035 | Unit | F011/012 | Exact trend boundaries<br>`test_exact_trend_thresholds[60-70-Improving]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS: all assertions passed |
| TC-036 | Unit | F011/012 | Exact trend boundaries<br>`test_exact_trend_thresholds[70-60-Declining]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS: all assertions passed |
| TC-037 | Unit | F011/012 | Exact trend boundaries<br>`test_exact_trend_thresholds[70-60.01-Stable]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS: all assertions passed |
| TC-038 | Unit | F011/012 | Exact trend boundaries<br>`test_exact_trend_thresholds[60-69.99-Stable]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS: all assertions passed |
| TC-039 | Unit | F013 | Intervention boundaries and reasons<br>`test_exact_intervention_thresholds_and_combined_reasons` | Score 50 and attendance 75 are normal; values below both thresholds plus decline yield all three reasons | PASS: all assertions passed |
| TC-040 | Integration | F001/002/003,SR004/006 | Account/profile input rejection<br>`test_password_and_profile_validation` | Short password, malformed hash, invalid IDs/semester, empty/long fields and invalid account roles are rejected | PASS: all assertions passed |
| TC-041 | Integration | F001,SR001 | Lockout expiry and recovery<br>`test_lockout_blocks_correct_password_then_expires` | Correct password is blocked during lockout, succeeds after 301 seconds and clears failed-attempt state | PASS: all assertions passed |
| TC-042 | Integration | NF005,SR006 | Snapshot recovery and rollback<br>`test_backup_restore_and_rollback` | Backup cannot overwrite source; restored snapshot passes integrity check; failed transaction is rolled back | PASS: all assertions passed |
| TC-043 | Integration | F004,NF006 | Legacy duplicate migration<br>`test_old_duplicate_seed_migration` | Initialization retains newest duplicate and reinstates record-key uniqueness | PASS: all assertions passed |
| TC-044 | Integration | F001,SR004 | Login and password storage<br>`test_authentication_and_password_storage` | Invalid login fails; salted hash verifies correct passwords only | PASS: all assertions passed |
| TC-045 | Integration | F015,SR001/002/003 | Student privacy and role denial<br>`test_student_privacy_and_write_denial` | Student reads only own records; unauthorized writes/reports/admin access are denied | PASS: all assertions passed |
| TC-046 | Integration | F004/005/017,SR005 | Attendance update and audit<br>`test_attendance_upsert_and_audit` | 4 of 4 classes yields 100 percent; one record remains and both operations are audited | PASS: all assertions passed |
| TC-047 | Integration | F004/006/007,SR006 | Invalid academic indicators<br>`test_invalid_writes_are_atomic[values0]` | Invalid counts, marks and nonfinite inputs fail without records or audit entries | PASS: all assertions passed |
| TC-048 | Integration | F004/006/007,SR006 | Invalid academic indicators<br>`test_invalid_writes_are_atomic[values1]` | Invalid counts, marks and nonfinite inputs fail without records or audit entries | PASS: all assertions passed |
| TC-049 | Integration | F004/006/007,SR006 | Invalid academic indicators<br>`test_invalid_writes_are_atomic[values2]` | Invalid counts, marks and nonfinite inputs fail without records or audit entries | PASS: all assertions passed |
| TC-050 | Integration | F004/006/007,SR006 | Invalid academic indicators<br>`test_invalid_writes_are_atomic[values3]` | Invalid counts, marks and nonfinite inputs fail without records or audit entries | PASS: all assertions passed |
| TC-051 | Integration | F004/006/007,SR006 | Invalid academic indicators<br>`test_invalid_writes_are_atomic[values4]` | Invalid counts, marks and nonfinite inputs fail without records or audit entries | PASS: all assertions passed |
| TC-052 | Integration | SR006 | Invalid links and period<br>`test_foreign_keys_and_period_validation` | Unknown student and invalid period are rejected | PASS: all assertions passed |
| TC-053 | Integration | F008/011/012/016 | Multi-subject historical aggregation<br>`test_period_aggregation_and_natural_order` | P10 follows P2; subject-average score is 68; no previous data and absent periods are handled | PASS: all assertions passed |
| TC-054 | Integration | F002/003,SR002 | Administration and account revocation<br>`test_admin_management_and_revocation` | Admin manages entities; deactivated accounts lose access; self-demotion and Faculty profile writes fail | PASS: all assertions passed |
| TC-055 | Integration | NF005/006 | Seed repeatability and backup<br>`test_seed_idempotency_and_backup` | Reseeding preserves credentials and 10 records; snapshot contains all records | PASS: all assertions passed |
| TC-056 | Integration | F014/016,SR006 | CSV filtering and formula escaping<br>`test_report_and_csv_injection` | P1 export excludes P2 and prefixes spreadsheet formula names | PASS: all assertions passed |
| TC-057 | Integration | F014/016,SR002 | Individual and at-risk exports<br>`test_individual_and_filtered_report` | Student 3 export has one row; risk-only export has students 3 and 4; Student role is denied | PASS: all assertions passed |
| TC-058 | Integration | F001,SR001 | Failed login counter<br>`test_lockout` | Five failed attempts are recorded | PASS: all assertions passed |
| TC-059 | Integration | NF001 | Normal synthetic query/summary load<br>`test_normal_load_performance` | 20 query-and-summary cycles complete in less than three seconds | PASS: all assertions passed |

## Original Test Plan traceability

| Original case | Current evidence |
|---|---|
| TC-AUTH-01 | Login/password service test and Student sign-in workflow |
| TC-SEC-01 | Student privacy/write denial and role-specific UI cases |
| TC-ATT-01 | Attendance upsert/audit; invalid attendance UI case |
| TC-MARK-01 | Invalid writes and numeric boundaries |
| TC-ANL-01 | Equal indicators and independent weight/boundary tests |
| TC-ANL-02 | Decline, exact trend boundaries and ordered period aggregation |
| TC-ANL-03 | Low attendance and combined intervention reasons |
| TC-DASH-01 | Student dashboard, support reasons, empty state, session checks |
| TC-DASH-02 | Faculty record/report flow, filter and historical view |
| TC-PERF-01 | Automated 20-summary load check; browser target remains MAN-02 |

## Manual acceptance cases not executed

| ID | Requirement | Check and steps | Expected outcome | Status |
|---|---|---|---|---|
| MAN-01 | NF004 | **Desktop visual acceptance**: Use Student, Faculty and Admin at 1366x768 and 1920x1080; inspect sign-in, forms, tables, charts and sidebar | All content readable; no clipping or overlap; controls match role | PENDING - user/team execution |
| MAN-02 | NF001 | **Browser load target**: Start the final app and time warm dashboard loads on the target machine; record data volume and timings | Dashboard loads within 3 seconds under normal project-test load | PENDING - user/team execution |
| MAN-03 | NF002 | **Demonstration readiness**: Start from documented commands on the demo machine and sign in under all roles | App remains usable during the planned demonstration | PENDING - user/team execution |
| MAN-04 | F014 | **Downloaded report acceptance**: Download a class and individual report; open in the intended spreadsheet application | Rows, encoding, filters and indicator labels match the chosen scope | PENDING - user/team execution |
| MAN-05 | NF005 | **Release backup sign-off**: Create a backup before release and confirm the selected snapshot and documented recovery location | Backup exists and the team can identify the recovery procedure | PENDING - user/team execution |
| MAN-06 | Course | **Final acceptance**: Team records tester, date, observed result and owner decision after manual checks | Owner signs off only after pending checks and defects are resolved | PENDING - user/team execution |

Record tester, actual date, observed result, evidence reference and PASS/FAIL for each manual case after execution. The course testing window is 2-6 November 2026. The execution timestamp above identifies this run; rerun after any further source changes.
