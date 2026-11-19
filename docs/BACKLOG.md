# Backlog and sprint plan

Prepared retrospectively on 29 October 2026 from the submitted SRS and deliverables image. Points are relative estimates. Owners below are proposed responsibility assignments, not a claim that those members authored this implementation. Confirm each member's GitHub handle before assigning issues.

| Item | Requirements | Points | Course sprint | Proposed owner | Acceptance |
|---|---|---:|---|---|---|
| B01 Authentication and role privacy | F001,F015,SR001–004 | 5 | 1: 19–23 Oct | Saransh | Valid login; student cannot see peers or edit data |
| B02 Student, subject and user management | F002,F003 | 5 | 1 | TB Akash | Admin can create/update entities and deactivate accounts |
| B03 Attendance and assessment persistence | F004–007,F017,SR005–006 | 5 | 1 | Sanapala Maneesh | Validated upserts, percentage calculation and audit |
| B04 Scoring and student dashboard | F008,F009,NF006 | 5 | 1 | Suhas MK | Correct weighted score, own history and charts |
| B05 Class trends and intervention | F010–013 | 5 | 2: 26–30 Oct | Suhas MK | Period aggregation, decline detection and explained flags |
| B06 Filters and report export | F014,F016 | 3 | 2 | TB Akash | Subject/period filtering; safe CSV download |
| B07 Regression, security and load tests; CI | NF001–004 | 5 | 2 | Sanapala Maneesh | Automated tests pass; UI workflows and permissions verified |
| B08 Backup, docs and release evidence | NF005 | 3 | 2 | Saransh | Backup/restore verified, docs complete, owner review and videos |

Code for B01–B07 and the backup/documentation portion of B08 is prepared in the completion branch. Approval, actual member PR contributions, videos and final development freeze require real team actions.

## GitHub Project setup

Create a board named Academic Performance Analytics, link this repository, and add the backlog issues. Recommended fields: Status (Todo/In progress/In review/Done), Story points (Number), Sprint (Sprint 1/Sprint 2), and Assignees. Copy estimates and proposed owners above after confirming member handles. Automation should move new issues to Todo and closed issues/merged PRs to Done. A linked project and its field values must be verified on GitHub before marking this deliverable complete.

Do not backdate issue creation or claim the optional 12–16 October dry run occurred. The course image permits backlog updates on 19 October; any later reconstruction should be described honestly during the final demo.

## GitHub evidence

Implementation PR: https://github.com/saransh1890/academic-performance-analytics/pull/4

Backlog issues created using the local GitHub sign-in after the connector rejected issue writes:

| Item | Issue |
|---|---|
| B01 | https://github.com/saransh1890/academic-performance-analytics/issues/5 |
| B02 | https://github.com/saransh1890/academic-performance-analytics/issues/6 |
| B03 | https://github.com/saransh1890/academic-performance-analytics/issues/7 |
| B04 | https://github.com/saransh1890/academic-performance-analytics/issues/8 |
| B05 | https://github.com/saransh1890/academic-performance-analytics/issues/9 |
| B06 | https://github.com/saransh1890/academic-performance-analytics/issues/10 |
| B07 | https://github.com/saransh1890/academic-performance-analytics/issues/11 |
| B08 | https://github.com/saransh1890/academic-performance-analytics/issues/12 |

Each issue contains story points, sprint mapping, proposed responsibility and acceptance criteria. Actual GitHub assignees remain unset pending confirmed handles and team acceptance. Creating or inspecting a Projects board is blocked by the local sign-in lacking the Projects scope (GitHub returned INSUFFICIENT_SCOPES). Repository push, issue creation and PR creation succeeded through local Git authentication.
