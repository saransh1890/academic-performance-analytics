# Part 3 testing deliverables

Executed evidence generated 2026-11-05T08:50:24+05:30. Source base: `bf35375`; the run manifest records any local source changes and SHA-256 hashes of the measured files. This reporting command does not push, start a server or open a browser.

**59/59 tests passed**, comprising 25 unit, 20 integration and 14 automated system-workflow cases. Total suite duration: 62.95 seconds.

Statement coverage: **97.32%**. Branch coverage: **91.94%**.

## Documents

- [Updated Test Case Document](Test_Case_Document.md)
- [Unit Test Report](Unit_Test_Report.md)
- [System Validation Report](System_Validation_Report.md)
- [Code Coverage Report](Code_Coverage_Report.md)
- [Branch Coverage Report](Branch_Coverage_Report.md)

## Reproduce

From the repository root, using Python 3.11:

```powershell
.\.venv\Scripts\python -m pip install -r requirements-test.txt
.\.venv\Scripts\python scripts/run_part3_checks.py
```

No seed, server startup or browser is required. The runner executes the tests once, generates raw and HTML coverage, and rebuilds all five documents from executed evidence. Reports are Markdown for direct review in GitHub. Original submitted DOCX baselines are preserved.

## Completion status

Automated test-case updates and all four report documents are included for owner review. Six manual acceptance cases are pending and explicitly recorded. Course testing dates are 2-6 November 2026; use the execution timestamp above and rerun after any further source changes. No Sprint 3 is claimed unless development actually spills over.

## Evidence and traceability

Raw JUnit, unit/system subsets, coverage JSON/XML, annotated HTML and a source SHA-256 manifest are under evidence/. The manifest identifies the exact source files, test instances, versions, actual test results and timings. Coverage is not inflated by excluding missing application branches. Tests use synthetic temporary records and no real student data or committed credentials.
