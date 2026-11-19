# As-built specification and traceability

Companion to the original SRS.docx, SAD.docx and Test_Plan.docx. Prepared 29 October 2026. The original documents define requirements, rather than instructions to the implementation agent.

## Architecture

Streamlit UI (`app.py`) calls application services (`services.py`). Services reload account permissions from SQLite, validate inputs and execute atomic writes with an audit event. Pure rules live in `analytics.py`; `database.py` manages connections, schema and backups. `seed_data.py` explicitly initializes synthetic demonstration accounts and records. There is no public REST API.

Accounts contain username, salted password hash, role, optional student link and active status. Students and subjects have stable numeric IDs. Academic records have a unique student/subject/period key. Foreign keys prevent orphan records. Audit entries store actor, UTC timestamp, operation and record change details; passwords are never logged. Login-attempt counters enforce five-attempt/five-minute throttling. Database access remains server-side.

## Traceability

| SRS requirement | Implementation | Automated evidence |
|---|---|---|
| F-001; SR-001/004 | PBKDF2 login, expiry, throttling | authentication/password, lockout, UI login tests |
| F-002/003 | Admin profile and subject upserts | admin management test; admin screen test |
| F-004/005 | Attended/conducted class percentage | attendance upsert test |
| F-006/007; SR-006 | Validated assessment writes | invalid writes/foreign key tests |
| F-008 | Weighted score | original analytics tests; aggregation test |
| F-009/015; SR-002/003 | Student-scoped service queries and dashboard | student privacy test; student UI test |
| F-010 | Class metrics and status chart | faculty UI and summary tests |
| F-011/012 | Ordered period averages and trend | aggregation/natural-order and trend tests |
| F-013 | Risk status with reasons | original intervention test |
| F-014 | CSV export with spreadsheet formula escaping | report export test; faculty reports UI test |
| F-016 | Subject and historical period filters | report and period tests |
| F-017; SR-005 | Atomic write + audit | attendance audit and invalid-write tests |
| NF-001 | Local query/summary load target | normal-load test (20 summaries under 3s); not a browser rendering benchmark |
| NF-002 | Documented startup and CI | app smoke tests; demo checklist |
| NF-003 | Service authorization; active-account checks | privacy, write denial, revocation tests |
| NF-004 | Wide layout, labels, chart ranges, empty states | Streamlit UI tests; manual visual review still required |
| NF-005 | Online SQLite backup and restore procedure | backup consistency test |
| NF-006 | Pure rules; deterministic aggregation | analytics and summary tests |

Identifiers above use the AAS- prefix from the original SRS.

## Clarifications and deviations

1. The SAD REST endpoints are a sketch. The submitted stack is Streamlit, so equivalent service functions implement login, data entry, analytics and reporting in-process. No REST server is claimed.
2. Attendance input uses class counts and stores the computed percentage, matching the submitted schema. Raw counts are not persisted.
3. All subjects receive equal weight within a period. Missing subjects are not imputed as zero. Latest available periods can differ by student; selecting a period makes comparisons explicit. Future institutional weighting or enrollment rules require a separate policy decision.
4. Periods use P1–P9999, with numeric ordering. Existing old period labels remain readable. No calendar-period model is claimed.
5. Account deactivation replaces destructive deletion, preserving audit and student records. Administrators can update profiles/subjects and reset account passwords; self-demotion/deactivation is blocked.
6. Faculty can access all classes in this course prototype. Course-assignment restrictions and external institutional integrations are outside the supplied requirements.
7. The prior prototype used a selectable demo role without authentication, had no record entry, and could compare different subjects as if they were consecutive periods. These are now addressed.
8. The original docs reference missing Mermaid sources. Sources are added alongside the existing rendered images. No claim is made that the existing images were regenerated.
9. Delivery is retrospective on 29 October. Sprint dates come from the provided course image; implementation commits and reviews must retain their actual dates. No historical team contribution, sprint video or review is fabricated.
10. The follow-up UI revision restricts the intervention-only checkbox to Faculty, gives Students personal metrics and own support feedback, adds individual-student report scope and filtered exports, and preloads existing academic values for editing. Attendance can be entered as counts or percentage; the stored schema is unchanged. See `UI_AND_REQUIREMENTS_REVIEW.md` for the original-document review and additions.

## Release acceptance

Run all tests, visually exercise each role, create a database backup, verify GitHub Actions on the PR, and have the owner review before merge. Record the two demonstration videos using docs/DEMO.md. The code is a single-instance project implementation; institutional production deployment requires a separate operational review and policy decisions.
