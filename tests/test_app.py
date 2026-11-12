import pytest
from pathlib import Path
import database
from seed_data import seed
from streamlit.testing.v1 import AppTest

@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setattr(database, 'DB_PATH', str(tmp_path / 'ui.db'))
    passwords = seed()
    return AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py', default_timeout=20), passwords


def login(app, role):
    at, passwords = app
    at.run()
    at.text_input[0].input(role)
    at.text_input[1].input(passwords[role])
    at.button[0].click().run()
    assert not at.exception
    return at


def test_login_and_student_dashboard(app):
    at = login(app,'student1')
    assert len(at.metric) == 4
    assert at.metric[0].label == 'Performance score'
    assert len(at.sidebar.radio[0].options) == 1
    assert any('Aarav' in m.value for m in at.markdown)
    assert 'Diya' not in str(at.dataframe[0].value)
    assert not at.checkbox
    assert not any(s.label == 'Student' for s in at.selectbox)
    at.sidebar.button[0].click().run()
    assert at.text_input[0].label == 'Username'


def test_faculty_record_flow(app):
    at = login(app,'faculty')
    at.sidebar.radio[0].set_value('Academic data').run()
    assert not at.exception
    at.text_input[0].input('P3').run()
    next(b for b in at.button if b.label == 'Save academic record').click().run()
    assert not at.exception
    assert at.success
    at.sidebar.radio[0].set_value('Reports').run()
    assert not at.exception
    assert at.metric[0].value == '5'


def test_admin_screen(app):
    at = login(app,'admin')
    at.sidebar.radio[0].set_value('Administration').run()
    assert not at.exception
    assert len(at.tabs) == 4


def test_faculty_intervention_filter_and_report_scope(app):
    at = login(app, 'faculty')
    toggle = next(c for c in at.checkbox if c.label == 'Show only students who need intervention')
    toggle.check().run()
    shown = at.dataframe[0].value
    assert len(shown) == 2
    assert set(shown.Status) == {'Needs Intervention'}
    assert at.metric[0].value == '5'  # Context metrics continue to describe the whole class.
    assert any(s.label == 'Report scope' for s in at.selectbox)
    toggle = next(c for c in at.checkbox if c.label == 'Show only students who need intervention')
    toggle.uncheck().run()
    assert len(at.dataframe[0].value) == 5


def test_admin_has_no_intervention_filter(app):
    at = login(app, 'admin')
    assert not at.checkbox
    at.sidebar.radio[0].set_value('Reports').run()
    assert not at.exception
    assert not at.checkbox


def test_student_sees_own_support_reasons(app):
    at = login(app, 'student3')
    assert not at.checkbox
    assert any('Low attendance' in w.value for w in at.warning)
    assert any('Declining performance' in w.value for w in at.warning)
    assert any('Rohan' in m.value for m in at.markdown)


def test_existing_marks_are_prefilled(app):
    at = login(app, 'faculty')
    at.sidebar.radio[0].set_value('Academic data').run()
    values = {n.label: n.value for n in at.number_input}
    assert values['Assignment / 100'] == 82
    assert values['Internal / 100'] == 80
    assert values['Exam / 100'] == 86
    assert values['Attendance (%)'] == 90
    next(b for b in at.button if b.label == 'Save academic record').click().run()
    assert not at.exception
    assert at.success


def test_subject_with_no_records_shows_empty_state(app):
    at = login(app, 'student1')
    at.selectbox(key='Dashboardsubject').set_value(2).run()
    assert not at.exception
    assert not at.metric
    assert at.info
    assert not at.checkbox


def test_failed_signin_stays_on_login(app):
    at,_ = app
    at.run()
    at.text_input[0].input('student1')
    at.text_input[1].input('incorrect')
    at.button[0].click().run()
    assert not at.exception
    assert at.error
    assert not at.metric


def test_expired_session_returns_to_login(app):
    import time
    at = login(app,'student1')
    at.session_state.last_activity = time.time() - 1801
    at.run()
    assert not at.exception
    assert at.text_input[0].label == 'Username'


def test_revoked_account_returns_to_login(app):
    at = login(app,'student1')
    with database.get_conn() as conn:
        conn.execute("UPDATE users SET active=0 WHERE username='student1'")
    at.run()
    assert not at.exception
    assert at.text_input[0].label == 'Username'


def test_invalid_attendance_shows_error(app):
    at = login(app,'faculty')
    at.sidebar.radio[0].set_value('Academic data').run()
    next(r for r in at.radio if r.label == 'Enter attendance using').set_value('Class counts').run()
    next(n for n in at.number_input if n.label == 'Classes attended').set_value(5)
    next(n for n in at.number_input if n.label == 'Classes conducted').set_value(4)
    next(b for b in at.button if b.label == 'Save academic record').click().run()
    assert not at.exception
    assert any('Attendance requires' in e.value for e in at.error)


def test_admin_management_forms_save(app):
    from services import authenticate, records_for
    at = login(app,'admin')
    at.sidebar.radio[0].set_value('Administration').run()
    next(n for n in at.number_input if n.label.startswith('Student ID')).set_value(6)
    next(t for t in at.text_input if t.label == 'Student name').input('Synthetic Test Student')
    next(b for b in at.button if b.label == 'Save student').click().run()
    assert not at.exception
    assert at.success
    next(n for n in at.number_input if n.label.startswith('Subject ID')).set_value(3)
    next(t for t in at.text_input if t.label == 'Subject code').input('TEST101')
    next(t for t in at.text_input if t.label == 'Subject name').input('Test Subject')
    next(b for b in at.button if b.label == 'Save subject').click().run()
    assert not at.exception
    assert at.success
    next(t for t in at.text_input if t.label == 'Account username').input('teststudent')
    next(t for t in at.text_input if t.label.startswith('New password')).input('synthetic-test-password')
    next(s for s in at.selectbox if s.label.startswith('Linked student')).set_value(6)
    next(b for b in at.button if b.label == 'Save account / reset password').click().run()
    assert not at.exception
    assert at.success
    new = authenticate('teststudent','synthetic-test-password')
    assert new is not None
    assert records_for(new).empty


def test_historical_filter_excludes_future_records(app):
    at = login(app,'faculty')
    at.selectbox(key='Dashboardperiod').set_value('P1').run()
    assert not at.exception
    assert set(at.dataframe[0].value.Period) == {'P1'}
    assert set(at.dataframe[1].value.Period) == {'P1'}


def test_intervention_filter_applies_to_trend_student_choices(app):
    at = login(app, 'faculty')
    next(c for c in at.checkbox if c.label.startswith('Show only')).check().run()
    trend_student = next(s for s in at.selectbox if s.label == 'Student')
    assert trend_student.options == ['3 · Rohan', '4 · Meera']
    assert not at.exception


def test_intervention_filter_limits_individual_report_options(app):
    at = login(app, 'faculty')
    at.sidebar.radio[0].set_value('Reports').run()
    next(c for c in at.checkbox if c.label.startswith('Show only')).check().run()
    scope = next(s for s in at.selectbox if s.label == 'Report scope')
    assert scope.options == ['Class summary', '3 · Rohan', '4 · Meera']
