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
    assert at.metric[0].value == '1'
    assert len(at.sidebar.radio[0].options) == 1
    assert 'Aarav' in str(at.dataframe[0].value)
    assert 'Diya' not in str(at.dataframe[0].value)
    at.sidebar.button[0].click().run()
    assert at.text_input[0].label == 'Username'


def test_faculty_record_flow(app):
    at = login(app,'faculty')
    at.sidebar.radio[0].set_value('Academic data').run()
    assert not at.exception
    at.text_input[0].input('P3')
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
