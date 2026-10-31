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
