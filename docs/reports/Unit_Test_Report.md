# Unit Test Report

Executed evidence generated 2026-11-05T08:50:24+05:30. Source base: `bf35375`; the run manifest records any local source changes and SHA-256 hashes of the measured files. This reporting command does not push, start a server or open a browser.

Python 3.11.9 on Windows; pytest 9.2.0, coverage 7.17.0, streamlit 1.66.1, pandas 3.1.0, plotly 7.1.0. Synthetic databases are isolated in temporary test directories.

**59/59 tests passed**, comprising 25 unit, 20 integration and 14 automated system-workflow cases. Total suite duration: 62.95 seconds.

## Unit scope

Unit cases exercise pure scoring, trend and intervention rules: the original six analytics cases plus independent weights, 0/100 boundaries, invalid/nonfinite values, exact trend thresholds and combined risk reasons. These are deterministic checks against explicit expected values. Authentication, database and UI tests are counted separately.

| Case | Expected result | Outcome | Seconds |
|---|---|---|---|
| TC-001: `test_performance_score` | All indicators at 80 produce score 80 | PASS | 0.0020 |
| TC-002: `test_declining_trend` | 75 to 64 is Declining | PASS | 0.0020 |
| TC-003: `test_improving_trend` | 60 to 72 is Improving | PASS | 0.0010 |
| TC-004: `test_stable_trend` | 70 to 75 is Stable | PASS | 0.0020 |
| TC-005: `test_low_attendance_triggers_intervention` | 60 percent attendance triggers a low-attendance reason | PASS | 0.0020 |
| TC-006: `test_invalid_score_inputs_rejected` | Score above 100 is rejected | PASS | 0.0020 |
| TC-021: `test_independent_weights_and_boundaries[inputs0-40]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS | 0.0020 |
| TC-022: `test_independent_weights_and_boundaries[inputs1-25]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS | 0.0030 |
| TC-023: `test_independent_weights_and_boundaries[inputs2-20]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS | 0.0020 |
| TC-024: `test_independent_weights_and_boundaries[inputs3-15]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS | 0.0020 |
| TC-025: `test_independent_weights_and_boundaries[inputs4-0]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS | 0.0020 |
| TC-026: `test_independent_weights_and_boundaries[inputs5-100]` | Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match | PASS | 0.0020 |
| TC-027: `test_nonfinite_and_invalid_scores[-0.01]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS | 0.0020 |
| TC-028: `test_nonfinite_and_invalid_scores[100.01]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS | 0.0020 |
| TC-029: `test_nonfinite_and_invalid_scores[inf]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS | 0.0020 |
| TC-030: `test_nonfinite_and_invalid_scores[-inf]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS | 0.0020 |
| TC-031: `test_nonfinite_and_invalid_scores[nan]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS | 0.0020 |
| TC-032: `test_nonfinite_and_invalid_scores[80]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS | 0.0020 |
| TC-033: `test_nonfinite_and_invalid_scores[None]` | Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError | PASS | 0.0030 |
| TC-034: `test_exact_trend_thresholds[None-80-No Previous Data]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS | 0.0020 |
| TC-035: `test_exact_trend_thresholds[60-70-Improving]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS | 0.0020 |
| TC-036: `test_exact_trend_thresholds[70-60-Declining]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS | 0.0020 |
| TC-037: `test_exact_trend_thresholds[70-60.01-Stable]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS | 0.0020 |
| TC-038: `test_exact_trend_thresholds[60-69.99-Stable]` | Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit | PASS | 0.0020 |
| TC-039: `test_exact_intervention_thresholds_and_combined_reasons` | Score 50 and attendance 75 are normal; values below both thresholds plus decline yield all three reasons | PASS | 0.0020 |

Evidence: [unit JUnit](evidence/unit-junit.xml), [full JUnit](evidence/junit.xml), [test-case document](Test_Case_Document.md). A passing unit suite does not establish browser usability or deployment readiness.
