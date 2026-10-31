# UI revision and original-requirements review

29 October 2026. Checked directly against `SRS.docx`, `SAD.docx` and `Test_Plan.docx`.

## Role-specific interface

The checkbox **Show only students who need intervention** is rendered only for Faculty. It is absent from Student and Admin dashboards and reports. Student accounts still see their own intervention status and reasons, as required by AAS-F-009/013/015 and SRS section 1.3. Removing the class filter does not remove the student's own support feedback.

Students see their own profile, weighted score, attendance, trend, selected assessment period, assessment history and an explanation of support flags. They cannot choose another student. Faculty see class counts, average performance and attendance, intervention counts, a filterable overview, student histories and exports. Admin retain overall analytics and administration tools.

## Presentation changes

- Added a shared light theme with navy text, teal accents, soft backgrounds, bordered metric cards, consistent rounded forms and responsive spacing.
- Added a two-column sign-in page with a product introduction and account-based access explanation. Developer seeding instructions remain in the README, outside the sign-in flow.
- Placed subject and assessment-period filters together. Added readable chart indicator names, consistent chart colors and labelled assessment tables.
- Moved calculation details into an expandable explanation. All intervention states continue to use text as well as color.
- Kept profile data in native Streamlit components. Custom HTML/CSS is static and contains no interpolated user data. No external fonts, image services or extra dependencies are needed.

## Additional workflow improvements

1. **Individual-student reports:** the SAD Reporting component calls for class or student exports. The previous UI only exported the whole class. Faculty and Admin can now select a named student or Class summary. Subject, period and the Faculty intervention filter apply to CSV output. Empty reports retain their headers. Students remain denied report access at the service boundary.
2. **Safer record editing:** student, subject and period selectors load existing marks and attendance before editing. Existing records default to percentage entry to preserve attendance without inventing class counts; raw historical class counts are not available in the submitted schema. New records support class counts or a percentage. Saving retains the existing validated upsert and audit transaction.
3. **Clear empty states:** a subject without records shows a role-appropriate message. A Faculty intervention filter with no matches states that no students meet the criteria. It does not hide the class context metrics.

## Functional acceptance review

| Original requirement | Current capability |
|---|---|
| AAS-F-001 | Sign-in before protected pages; service authorization and inactivity expiry |
| AAS-F-002 | Admin creates/updates student profiles |
| AAS-F-003 | Admin creates/updates subjects |
| AAS-F-004/005 | Faculty creates/updates attendance; class-count percentage calculation |
| AAS-F-006/007 | Faculty creates/updates assignment, internal and exam marks |
| AAS-F-008 | Submitted weighted performance formula |
| AAS-F-009 | Personal student dashboard, assessment history and metrics |
| AAS-F-010 | Class metrics, overview table and chart |
| AAS-F-011/012 | Ordered assessment-period trends and decline detection |
| AAS-F-013 | Explained intervention flags; own status remains visible to students |
| AAS-F-014 | Authorized class and individual-student CSV reports |
| AAS-F-015 | Student-scoped service queries; no peer selector or class filter |
| AAS-F-016 | Subject and period filtering for dashboards and reports |
| AAS-F-017 | Actor, UTC timestamp and academic changes audited atomically |

All 17 functional requirements have implementation paths. The original test-plan cases cover login, role denial, attendance, invalid marks, score, trends, intervention flags and Student/Faculty dashboards; these have automated evidence. Additional regression cases cover Faculty-only filter visibility, individual/filtered report contents, existing-record prefilling, Student support feedback and empty states.

## What this does not establish

- SAD section 5 is an API sketch. Equivalent service operations are implemented in the submitted Streamlit architecture; a public REST server has not been delivered. This is a documented design deviation, not a claim of endpoint compatibility.
- The normal-load test measures local database-to-summary work. A browser load within three seconds and visual usability on the final display still need manual verification. No browser preview or server was started for this revision, at the user's request.
- Availability during the demonstration depends on the team starting and checking the app. Backups are implemented and tested, but the team must create one before final release and follow the recovery procedure if needed.
- The linked GitHub Project is blocked by missing Projects permission. Backlog issues exist, but actual team assignments, member-authored PRs, owner review, two real sprint recordings and final development freeze remain course-delivery tasks. These cannot be replaced by application code or scripts.

See `IMPLEMENTATION.md` for full security/non-functional traceability, `VALIDATION.md` for test evidence, and `DELIVERY.md` for remaining submission work. Original DOCX files are preserved as submitted baselines.
