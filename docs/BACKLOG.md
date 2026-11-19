# Backlog responsibilities and sprint plan

Updated locally on 5 November 2026 to match the actual role exchange. Suhas owns analytics/reporting; Akash owns UI/integration. These responsibility mappings do not rewrite PR authorship or set GitHub assignees automatically.

## Confirmed contribution map

| Member | GitHub account | Actual contribution | Merged PR |
|---|---|---|---|
| Saransh Mittal | saransh1890 | Database foundation, authentication and accounts | #13 |
| Sanapala Maneesh | Maneesh36 | Student/subject services, attendance/marks writes, validation and audit | #14 |
| Suhas MK | Suhasmk124 | Scoring, period aggregation, trends, intervention and filtered reports | #15 |
| TB Akash | AkashBalaji3107 | UI, role-specific pages, forms, styling, integration tests, CI and documentation integration | #16 |

Suhas also submitted Part 3 testing reports in PR #17. The revised SRS/SAD/Test Plan are recommended for Akash to upload as documentation/integration work, with Saransh reviewing and merging after team verification. Ownership does not imply exclusive authorship of every supporting test or document.

## Backlog and sprint allocation

Points are relative estimates from the original plan. Dates are course sprint windows, not claims about individual commit dates. Paired owners identify a service/UI split. GitHub issue assignees and board fields must be updated separately to match this local mapping.

| Item | Requirements | Points | Course sprint | Current responsibility | Acceptance |
|---|---|---:|---|---|---|
| B01 Authentication and role privacy | F001,F015,SR001-004 | 5 | Sprint 1: 19-23 Oct | Saransh | Valid login, active role checks and Student peer exclusion |
| B02 Student, subject and account management | F002,F003 | 5 | Sprint 1 | Maneesh: profiles/subjects; Saransh: accounts; Akash: forms | Authorized management and Student linking |
| B03 Attendance and assessments | F004-007,F017,SR005-006 | 5 | Sprint 1 | Maneesh: records/audit; Akash: entry UI | Validated percentage and marks upserts with atomic audit |
| B04 Scoring and Student dashboard | F008,F009,NF006 | 5 | Sprint 1 | Suhas: score; Akash: Student UI | Correct formula and own history/metrics |
| B05 Class trends and intervention | F010-013 | 5 | Sprint 2: 26-30 Oct | Suhas: analysis; Akash: class UI | Ordered periods, explained flags and Faculty-only filter |
| B06 Filters and reports | F014,F016 | 3 | Sprint 2 | Suhas: query/export; Akash: controls | Correct subject/period/student scope and safe CSV |
| B07 Regression and CI | NF001-004 | 5 | Sprint 2 | Akash: UI/integration/CI; Suhas: analytics/report evidence; Maneesh: record tests | Recorded test outcomes and completed manual acceptance |
| B08 Backup, documentation and release | NF005; course deliverables | 3 | Sprint 2 | Saransh: release acceptance; Akash: final document integration; team: demos | Backup, finalized docs, recordings, reviews and freeze |

## GitHub evidence and remaining board work

Implementation PRs: #13 Saransh, #14 Maneesh, #15 Suhas, #16 Akash. PR #4 is the original consolidated reference and is not the four-member integration record. Part 3 reports are in PR #17.

Backlog issues B01-B08 correspond to issues #5-#12. They contain story estimates and acceptance criteria. The latest audit found no actual assignees and all issues open. This local edit does not change GitHub. Assign issues to the confirmed handles, reflect service/UI work honestly, and close only accepted work. Link the repository to a Project with Status, Story points, Sprint and Assignees fields; show Sprint 1 and Sprint 2 explicitly. Project API access was blocked by missing Projects permission at the time of checking.

Record actual dates. Do not backdate issues or claim the optional dry run occurred. Sprint 1 needs a one-minute working-outcome video and Sprint 2 needs a two-minute working-outcome video. Owner acceptance, manual checks and development freeze remain team actions.
