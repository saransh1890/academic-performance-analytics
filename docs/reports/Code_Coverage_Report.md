# Code Coverage Report

Executed evidence generated 2026-11-05T08:50:24+05:30. Source base: `bf35375`; the run manifest records any local source changes and SHA-256 hashes of the measured files. This reporting command does not push, start a server or open a browser.

**Statement coverage: 97.32% (435/447 executable statements).**

## Measurement scope

Measured all six production Python modules: analytics.py, app.py, database.py, seed_data.py, services.py and ui.py. Tests, scripts, virtual environment and temporary files are excluded by .coveragerc. UI execution is included through thread-aware AppTest measurement. Third-party libraries, CSS rendering, TOML/YAML execution and manual workflows are outside Python statement coverage.

| Production module | Covered statements | Total statements | Statement coverage | Missing lines |
|---|---:|---:|---:|---|
| analytics.py | 24 | 24 | 100.00% | None |
| app.py | 201 | 207 | 97.10% | 126, 161, 231, 232, 233, 234 |
| database.py | 29 | 29 | 100.00% | None |
| seed_data.py | 20 | 26 | 76.92% | 32, 33, 34, 35, 36, 37 |
| services.py | 148 | 148 | 100.00% | None |
| ui.py | 13 | 13 | 100.00% | None |

## Interpretation and reproduction

Uncovered lines above are measured gaps, not omitted from the denominator. Review them in the [annotated HTML report](evidence/coverage-html/index.html); consult the system report for manual acceptance gaps. No minimum percentage is specified in the supplied Part 3 PDF, so no unsupported coverage threshold is claimed.

Run `python scripts/run_part3_checks.py` after installing requirements-test.txt. Raw evidence: [coverage JSON](evidence/coverage-data.json), [Cobertura XML](evidence/cobertura.xml), [run/source manifest](evidence/run-manifest.json).
