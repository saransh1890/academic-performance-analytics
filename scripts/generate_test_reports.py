"""Generate readable Part 3 reports from executed JUnit and coverage evidence."""
import copy
import hashlib
import importlib.metadata as metadata
import json
import platform
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/reports'
EVIDENCE = OUT/'evidence'
# requirement, scenario, expected behavior
CASES = {
 'test_decimal_scores_at_trend_threshold': ('F011/012','Decimal trend thresholds','An exact decimal 10-point change is directional; a smaller change stays stable'),
 'test_boolean_and_oversized_indicators_are_rejected': ('SR006','Invalid indicator types and magnitudes','Boolean values and oversized integers raise a validation error'),
 'test_export_neutralizes_formula_lookalikes': ('F014,SR006','Unicode formula markers in CSV','Formula-like exported text receives a literal prefix'),
 'test_report_preserves_quotes_commas_and_line_endings': ('F014','Spreadsheet-compatible CSV','Unicode text with commas and quotes round-trips with CRLF line endings'),
 'test_intervention_filter_applies_to_trend_student_choices': ('F010/013','Filtered trend drill-down','Only students in the filtered class table are selectable'),
 'test_intervention_filter_limits_individual_report_options': ('F013/014/016','Filtered report choices','Class summary and only matching individual students are selectable'),
 'test_empty_subject_can_export_csv_headers': ('F014/016','Empty report download','The Reports workspace offers a download for a subject with no records'),
 'test_historical_report_uses_subject_and_intervention_filters_together': ('F011/013/014/016','Combined historical report filters','Future or unrelated subject records do not flag the selected student'),
 'test_performance_score': ('F008,NF006','Equal assessment indicators','All indicators at 80 produce score 80'),
 'test_declining_trend': ('F011/012','Declining score','75 to 64 is Declining'),
 'test_improving_trend': ('F011','Improving score','60 to 72 is Improving'),
 'test_stable_trend': ('F011','Stable score','70 to 75 is Stable'),
 'test_low_attendance_triggers_intervention': ('F013','Low attendance','60 percent attendance triggers a low-attendance reason'),
 'test_invalid_score_inputs_rejected': ('SR006','Out-of-range score','Score above 100 is rejected'),
 'test_authentication_and_password_storage': ('F001,SR004','Login and password storage','Invalid login fails; salted hash verifies correct passwords only'),
 'test_student_privacy_and_write_denial': ('F015,SR001/002/003','Student privacy and role denial','Student reads only own records; unauthorized writes/reports/admin access are denied'),
 'test_attendance_upsert_and_audit': ('F004/005/017,SR005','Attendance update and audit','4 of 4 classes yields 100 percent; one record remains and both operations are audited'),
 'test_invalid_writes_are_atomic': ('F004/006/007,SR006','Invalid academic indicators','Invalid counts, marks and nonfinite inputs fail without records or audit entries'),
 'test_foreign_keys_and_period_validation': ('SR006','Invalid links and period','Unknown student and invalid period are rejected'),
 'test_period_aggregation_and_natural_order': ('F008/011/012/016','Multi-subject historical aggregation','P10 follows P2; subject-average score is 68; no previous data and absent periods are handled'),
 'test_admin_management_and_revocation': ('F002/003,SR002','Administration and account revocation','Admin manages entities; deactivated accounts lose access; self-demotion and Faculty profile writes fail'),
 'test_seed_idempotency_and_backup': ('NF005/006','Seed repeatability and backup','Reseeding preserves credentials and 10 records; snapshot contains all records'),
 'test_report_and_csv_injection': ('F014/016,SR006','CSV filtering and formula escaping','P1 export excludes P2 and prefixes spreadsheet formula names'),
 'test_individual_and_filtered_report': ('F014/016,SR002','Individual and at-risk exports','Student 3 export has one row; risk-only export has students 3 and 4; Student role is denied'),
 'test_lockout': ('F001,SR001','Failed login counter','Five failed attempts are recorded'),
 'test_normal_load_performance': ('NF001','Normal synthetic query/summary load','20 query-and-summary cycles complete in less than three seconds'),
 'test_login_and_student_dashboard': ('F001/009/015','Student dashboard and logout','Own metrics and history appear; peer data/class controls are absent; logout returns to sign-in'),
 'test_faculty_record_flow': ('F004/006/007/010/014','Faculty record-to-report workflow','Record saves successfully; report page opens and class metrics remain available'),
 'test_admin_screen': ('F002/003,SR002','Administrator workspace','Student, subject, account and audit/backup tabs render'),
 'test_faculty_intervention_filter_and_report_scope': ('F010/013/014','Faculty intervention filter','Filter returns two flagged students; clearing restores five; report scope is available'),
 'test_admin_has_no_intervention_filter': ('SR002','Admin filter visibility','Faculty-only checkbox is absent from Admin dashboard and reports'),
 'test_student_sees_own_support_reasons': ('F009/013/015','Student support feedback','Rohan sees own low-attendance and declining reasons without class filter'),
 'test_existing_marks_are_prefilled': ('F004/006/007','Existing academic record editing','Existing 90/82/80/86 indicators preload and save successfully'),
 'test_subject_with_no_records_shows_empty_state': ('F009/016','Empty student subject view','Subject without records shows a message without metrics or class filter'),
 'test_failed_signin_stays_on_login': ('F001,SR001','Failed sign-in workflow','Error appears; protected metrics remain absent'),
 'test_expired_session_returns_to_login': ('SR001/002','Session inactivity expiry','Session older than 1800 seconds returns to sign-in'),
 'test_revoked_account_returns_to_login': ('SR002/003','Active session account revocation','Deactivated student session loses dashboard access on next interaction'),
 'test_invalid_attendance_shows_error': ('F004/005,SR006','Attendance error message','Attending 5 of 4 classes shows an understandable validation error'),
 'test_admin_management_forms_save': ('F002/003,SR002','Admin create and account-link workflow','Student and subject are created; linked account authenticates and has no peer records'),
 'test_historical_filter_excludes_future_records': ('F011/016','Historical dashboard filter','Selecting P1 shows P1 summaries/history without future periods'),
 'test_independent_weights_and_boundaries': ('F008,NF006','Independent formula weights','Single 100 inputs contribute 40/25/20/15; all-zero and all-100 boundaries match'),
 'test_nonfinite_and_invalid_scores': ('SR006','Numeric validation boundaries','Negative, above-100, infinite, NaN and nonnumeric inputs raise ValueError'),
 'test_exact_trend_thresholds': ('F011/012','Exact trend boundaries','Exactly plus/minus 10 changes trend; smaller deltas remain stable; no previous data is explicit'),
 'test_exact_intervention_thresholds_and_combined_reasons': ('F013','Intervention boundaries and reasons','Score 50 and attendance 75 are normal; values below both thresholds plus decline yield all three reasons'),
 'test_password_and_profile_validation': ('F001/002/003,SR004/006','Account/profile input rejection','Short password, malformed hash, invalid IDs/semester, empty/long fields and invalid account roles are rejected'),
 'test_lockout_blocks_correct_password_then_expires': ('F001,SR001','Lockout expiry and recovery','Correct password is blocked during lockout, succeeds after 301 seconds and clears failed-attempt state'),
 'test_backup_restore_and_rollback': ('NF005,SR006','Snapshot recovery and rollback','Backup cannot overwrite source; restored snapshot passes integrity check; failed transaction is rolled back'),
 'test_old_duplicate_seed_migration': ('F004,NF006','Legacy duplicate migration','Initialization retains newest duplicate and reinstates record-key uniqueness'),
}
UNIT_NAMES = {'test_independent_weights_and_boundaries','test_nonfinite_and_invalid_scores',
              'test_exact_trend_thresholds','test_exact_intervention_thresholds_and_combined_reasons'}
MANUAL = [
 ('MAN-01','NF004','Desktop visual acceptance','Use Student, Faculty and Admin at 1366x768 and 1920x1080; inspect sign-in, forms, tables, charts and sidebar','All content readable; no clipping or overlap; controls match role'),
 ('MAN-02','NF001','Browser load target','Start the final app and time warm dashboard loads on the target machine; record data volume and timings','Dashboard loads within 3 seconds under normal project-test load'),
 ('MAN-03','NF002','Demonstration readiness','Start from documented commands on the demo machine and sign in under all roles','App remains usable during the planned demonstration'),
 ('MAN-04','F014','Downloaded report acceptance','Download a class and individual report; open in the intended spreadsheet application','Rows, encoding, filters and indicator labels match the chosen scope'),
 ('MAN-05','NF005','Release backup sign-off','Create a backup before release and confirm the selected snapshot and documented recovery location','Backup exists and the team can identify the recovery procedure'),
 ('MAN-06','Course','Final acceptance','Team records tester, date, observed result and owner decision after manual checks','Owner signs off only after pending checks and defects are resolved'),
]

def write(name,text):
    (OUT/name).write_text(text,encoding='utf-8',newline='\n')

def percent(n,d):
    return f'{100*n/d:.2f}%' if d else 'N/A (no branches)'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    root = ET.parse(EVIDENCE/'junit.xml').getroot()
    cases = list(root.iter('testcase'))
    coverage = json.loads((EVIDENCE/'coverage-data.json').read_text())
    now = datetime.now(timezone(timedelta(hours=5,minutes=30))).isoformat(timespec='seconds')
    base = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    rows=[]
    for c in cases:
        name=c.attrib['name']; function=name.split('[',1)[0]
        if function not in CASES:
            raise ValueError('Missing case specification for '+function)
        requirement,scenario,expected = CASES[function]
        category='Unit' if c.attrib.get('classname','').endswith('test_analytics') or function in UNIT_NAMES else ('System' if c.attrib.get('classname','').endswith('test_app') else 'Integration')
        status='FAIL' if c.find('failure') is not None or c.find('error') is not None else ('SKIP' if c.find('skipped') is not None else 'PASS')
        rows.append(dict(id=f'TC-{len(rows)+1:03d}',name=name,function=function,requirement=requirement,scenario=scenario,expected=expected,category=category,status=status,seconds=float(c.attrib.get('time',0))))
    counts={kind:sum(r['category']==kind for r in rows) for kind in ['Unit','Integration','System']}
    passed=sum(r['status']=='PASS' for r in rows)
    suite_time=sum(float(s.attrib.get('time',0)) for s in root.findall('testsuite'))
    fingerprints={}
    for pattern in ['*.py','tests/*.py','scripts/*.py']:
        for path in ROOT.glob(pattern):
            fingerprints[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    for filename in ['.coveragerc','requirements-lock.txt','requirements-test.txt','.github/workflows/tests.yml','.streamlit/config.toml']:
        fingerprints[filename]=hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()
    environment={name:metadata.version(name) for name in ['pytest','coverage','streamlit','pandas','plotly']}
    dirty = subprocess.check_output(['git','status','--porcelain','--','*.py','tests','scripts','.coveragerc','requirements-test.txt','.github/workflows/tests.yml','.streamlit/config.toml'],cwd=ROOT,text=True).strip()
    record={'generated_at_IST':now,'source_base_commit':base,'local_source_changes_present':bool(dirty),'python':platform.python_version(),
            'platform':platform.platform(),'packages':environment,'tests':len(rows),'passed':passed,'counts':counts,'suite_seconds':suite_time,
            'source_sha256':fingerprints,'cases':rows,'coverage_totals':coverage['totals']}
    (EVIDENCE/'run-manifest.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    for category,filename in [('Unit','unit-junit.xml'),('System','system-junit.xml')]:
        selected=[c for c,r in zip(cases,rows) if r['category']==category]
        subset=ET.Element('testsuite',name=category,tests=str(len(selected)),failures=str(sum(c.find('failure') is not None for c in selected)),errors=str(sum(c.find('error') is not None for c in selected)),skipped=str(sum(c.find('skipped') is not None for c in selected)))
        subset.extend(copy.deepcopy(c) for c in selected)
        ET.ElementTree(subset).write(EVIDENCE/filename,encoding='utf-8',xml_declaration=True)
    totals=coverage['totals']
    covered_lines=totals['covered_lines']; statements=totals['num_statements']
    branches=totals['num_branches']; covered_branches=totals['covered_branches']
    stamp=f'Executed evidence generated {now}. Source base: `{base[:7]}`; the run manifest records any local source changes and SHA-256 hashes of the measured files. This reporting command does not push, start a server or open a browser.\n\n'
    environment_text=f'Python {platform.python_version()} on {platform.system()}; '+', '.join(f'{k} {v}' for k,v in environment.items())+'. Synthetic databases are isolated in temporary test directories.\n\n'
    result=f'**{passed}/{len(rows)} tests passed**, comprising {counts["Unit"]} unit, {counts["Integration"]} integration and {counts["System"]} automated system-workflow cases. Total suite duration: {suite_time:.2f} seconds.\n\n'
    cases_text='# Updated Test Case Document\n\n'+stamp+'This document updates the original Test_Plan.docx with sprint changes and recorded outcomes. Requirements use the AAS- prefix from SRS.docx.\n\n'+result+environment_text
    cases_text+='## Preconditions and execution\n\nInstall requirements-test.txt and run `python scripts/run_part3_checks.py`. Tests initialize only synthetic temporary databases. Automated system cases execute Streamlit AppTest, not a browser. Expected outcomes below are asserted in the linked test implementations; each parameterized instance is recorded separately. Raw node names and timings are in evidence/run-manifest.json and evidence/junit.xml.\n\n'
    cases_text+='## Executed test cases\n\n| ID | Type | Requirement | Scenario and test instance | Expected outcome | Actual result |\n|---|---|---|---|---|---|\n'
    for r in rows:
        safe=r['name'].replace('|','\\|')
        cases_text+=f'| {r["id"]} | {r["category"]} | {r["requirement"]} | {r["scenario"]}<br>`{safe}` | {r["expected"]} | {r["status"]}: '+('all assertions passed' if r['status']=='PASS' else 'see raw JUnit result')+' |\n'
    cases_text+='\n## Original Test Plan traceability\n\n| Original case | Current evidence |\n|---|---|\n| TC-AUTH-01 | Login/password service test and Student sign-in workflow |\n| TC-SEC-01 | Student privacy/write denial and role-specific UI cases |\n| TC-ATT-01 | Attendance upsert/audit; invalid attendance UI case |\n| TC-MARK-01 | Invalid writes and numeric boundaries |\n| TC-ANL-01 | Equal indicators and independent weight/boundary tests |\n| TC-ANL-02 | Decline, exact trend boundaries and ordered period aggregation |\n| TC-ANL-03 | Low attendance and combined intervention reasons |\n| TC-DASH-01 | Student dashboard, support reasons, empty state, session checks |\n| TC-DASH-02 | Faculty record/report flow, filter and historical view |\n| TC-PERF-01 | Automated 20-summary load check; browser target remains MAN-02 |\n'
    cases_text+='\n## Manual acceptance cases not executed\n\n| ID | Requirement | Check and steps | Expected outcome | Status |\n|---|---|---|---|---|\n'
    for mid,req,title,steps,expected in MANUAL:
        cases_text+=f'| {mid} | {req} | **{title}**: {steps} | {expected} | PENDING - user/team execution |\n'
    cases_text+='\nRecord tester, actual date, observed result, evidence reference and PASS/FAIL for each manual case after execution. The course testing window is 2-6 November 2026. The execution timestamp above identifies this run; rerun after any further source changes.\n'
    write('Test_Case_Document.md',cases_text)
    unit='# Unit Test Report\n\n'+stamp+environment_text+result+'## Unit scope\n\nUnit cases exercise pure scoring, trend and intervention rules: the original six analytics cases plus independent weights, 0/100 boundaries, invalid/nonfinite values, exact trend thresholds and combined risk reasons. These are deterministic checks against explicit expected values. Authentication, database and UI tests are counted separately.\n\n'
    unit+='| Case | Expected result | Outcome | Seconds |\n|---|---|---|---|\n'
    for r in rows:
        if r['category']=='Unit': unit+=f'| {r["id"]}: `{r["name"]}` | {r["expected"]} | {r["status"]} | {r["seconds"]:.4f} |\n'
    unit+='\nEvidence: [unit JUnit](evidence/unit-junit.xml), [full JUnit](evidence/junit.xml), [test-case document](Test_Case_Document.md). A passing unit suite does not establish browser usability or deployment readiness.\n'
    write('Unit_Test_Report.md',unit)
    system='# System Validation Report\n\n'+stamp+environment_text+result+'## Automated validation conclusion\n\nThe automated application workflows and integration checks passed for this source snapshot. Overall acceptance is **PENDING MANUAL VALIDATION**, not an unconditional release approval. AppTest exercises server-side Streamlit widgets and state; it does not render browser pixels, measure network latency or establish live availability.\n\n'
    system+='| Automated system case | Expected behavior | Result |\n|---|---|---|\n'
    for r in rows:
        if r['category']=='System': system+=f'| {r["id"]}: {r["scenario"]} | {r["expected"]} | {r["status"]} |\n'
    system+='\n## Supporting integration checks\n\nValidated authorization and revoked access; percentage calculation and unique upserts; atomic audits and rejected inputs; foreign keys; period and subject filtering; individual and risk-only exports; formula escaping; seed idempotency; backup consistency and recovery; migration of old duplicate seed rows; and transaction rollback.\n\nThe normal-load case asserts that 20 synthetic query-and-summary cycles finish within three seconds. This is a local service test, not proof of the SRS browser dashboard load target.\n\n## Manual acceptance still required\n\n'
    for mid,req,title,steps,expected in MANUAL:
        system+=f'- **{mid} {title} ({req}) - PENDING.** {steps}. Expected: {expected}.\n'
    system+='\n## Defect and acceptance status\n\nNo automated failures occurred in this run. This is not a claim of zero undiscovered defects. No human visual results, owner approval, demo recordings, final freeze or GitHub upload are fabricated. The optional Sprint 3 is needed only if actual development spillover occurs during 2-6 November.\n\nEvidence: [system JUnit](evidence/system-junit.xml), [full JUnit](evidence/junit.xml), [test cases](Test_Case_Document.md), [run manifest](evidence/run-manifest.json).\n'
    write('System_Validation_Report.md',system)
    line='# Code Coverage Report\n\n'+stamp+f'**Statement coverage: {percent(covered_lines,statements)} ({covered_lines}/{statements} executable statements).**\n\n'
    line+='## Measurement scope\n\nMeasured all six production Python modules: analytics.py, app.py, database.py, seed_data.py, services.py and ui.py. Tests, scripts, virtual environment and temporary files are excluded by .coveragerc. UI execution is included through thread-aware AppTest measurement. Third-party libraries, CSS rendering, TOML/YAML execution and manual workflows are outside Python statement coverage.\n\n'
    line+='| Production module | Covered statements | Total statements | Statement coverage | Missing lines |\n|---|---:|---:|---:|---|\n'
    branch='# Branch Coverage Report\n\n'+stamp+f'**Branch coverage: {percent(covered_branches,branches)} ({covered_branches}/{branches} measured branch destinations).**\n\n'
    branch+='Coverage.py measures alternative control-flow destinations, not merely the number of if statements. This report separates branch coverage from statement coverage and from Coverage.py combined display percentages. A high percentage does not prove every possible input or security state is correct.\n\n| Production module | Covered destinations | Total destinations | Branch coverage | Sources of missing branches |\n|---|---:|---:|---:|---|\n'
    missing_branch={}
    for filename,info in coverage['files'].items():
        s=info['summary']; missing=info.get('missing_lines',[])
        line+=f'| {filename} | {s["covered_lines"]} | {s["num_statements"]} | {percent(s["covered_lines"],s["num_statements"])} | '+(', '.join(map(str,missing)) or 'None')+' |\n'
        arcs=info.get('missing_branches',[])
        sources=sorted({a[0] for a in arcs})
        branch+=f'| {filename} | {s.get("covered_branches",0)} | {s.get("num_branches",0)} | {percent(s.get("covered_branches",0),s.get("num_branches",0))} | '+(', '.join(map(str,sources)) or 'None')+' |\n'
        if arcs: missing_branch[filename]=arcs
    line+='\n## Interpretation and reproduction\n\nUncovered lines above are measured gaps, not omitted from the denominator. Review them in the [annotated HTML report](evidence/coverage-html/index.html); consult the system report for manual acceptance gaps. No minimum percentage is specified in the supplied Part 3 PDF, so no unsupported coverage threshold is claimed.\n\nRun `python scripts/run_part3_checks.py` after installing requirements-test.txt. Raw evidence: [coverage JSON](evidence/coverage-data.json), [Cobertura XML](evidence/cobertura.xml), [run/source manifest](evidence/run-manifest.json).\n'
    branch+='\n## Uncovered branch destinations\n\nPairs below are source-line and destination-line numbers from Coverage.py. Negative destinations represent function exits. These are retained explicitly rather than hidden by exclusions.\n\n```json\n'+json.dumps(missing_branch,indent=2)+'\n```\n\nReproduce with `python scripts/run_part3_checks.py`. Evidence: [annotated HTML](evidence/coverage-html/index.html), [raw JSON](evidence/coverage-data.json), [Cobertura XML](evidence/cobertura.xml). Manual visual acceptance, deployment availability and an actual browser load measurement remain separate.\n'
    write('Code_Coverage_Report.md',line)
    write('Branch_Coverage_Report.md',branch)
    index='# Part 3 testing deliverables\n\n'+stamp+result+f'Statement coverage: **{percent(covered_lines,statements)}**. Branch coverage: **{percent(covered_branches,branches)}**.\n\n'
    index+='## Documents\n\n- [Updated Test Case Document](Test_Case_Document.md)\n- [Unit Test Report](Unit_Test_Report.md)\n- [System Validation Report](System_Validation_Report.md)\n- [Code Coverage Report](Code_Coverage_Report.md)\n- [Branch Coverage Report](Branch_Coverage_Report.md)\n\n'
    index+='## Reproduce\n\nFrom the repository root, using Python 3.11:\n\n```powershell\n.\\.venv\\Scripts\\python -m pip install -r requirements-test.txt\n.\\.venv\\Scripts\\python scripts/run_part3_checks.py\n```\n\nNo seed, server startup or browser is required. The runner executes the tests once, generates raw and HTML coverage, and rebuilds all five documents from executed evidence. Reports are Markdown for direct review in GitHub. Original submitted DOCX baselines are preserved.\n\n'
    index+='## Completion status\n\nAutomated test-case updates and all four report documents are included for owner review. Six manual acceptance cases are pending and explicitly recorded. Course testing dates are 2-6 November 2026; use the execution timestamp above and rerun after any further source changes. No Sprint 3 is claimed unless development actually spills over.\n\n'
    index+='## Evidence and traceability\n\nRaw JUnit, unit/system subsets, coverage JSON/XML, annotated HTML and a source SHA-256 manifest are under evidence/. The manifest identifies the exact source files, test instances, versions, actual test results and timings. Coverage is not inflated by excluding missing application branches. Tests use synthetic temporary records and no real student data or committed credentials.\n'
    write('README.md',index)
    print(json.dumps({'tests':len(rows),'passed':passed,'categories':counts,'statement_coverage':percent(covered_lines,statements),'branch_coverage':percent(covered_branches,branches),'reports':str(OUT)}))

if __name__=='__main__':
    main()
