import pytest

import database
from seed_data import seed
from services import administration, authenticate, records_for, save_record, save_student, save_subject


@pytest.fixture
def principals(tmp_path, monkeypatch):
    monkeypatch.setattr(database, 'DB_PATH', str(tmp_path / 'records.db'))
    passwords = seed()
    return {role: authenticate(role, passwords[role]) for role in ('admin', 'faculty')}


@pytest.mark.parametrize('student,semester', [(1.5, 3), (1, 3.5), (True, 3)])
def test_student_validation_preserves_existing_profile(principals, student, semester):
    with pytest.raises(ValueError):
        save_student(principals['admin'], student, 'Changed', 'CSE', semester)
    assert records_for(principals['faculty']).iloc[0]['name'] == 'Aarav'
    assert administration(principals['admin'])[1].empty


@pytest.mark.parametrize('subject,code', [(2.5, 'CHANGE'), (2, None)])
def test_subject_validation_rejects_partial_ids_and_missing_text(principals, subject, code):
    with pytest.raises(ValueError):
        save_subject(principals['admin'], subject, code, 'Bad update')
    assert administration(principals['admin'])[1].empty
    with pytest.raises(ValueError):
        records_for(principals['faculty'], subject_id=2.5)


@pytest.mark.parametrize('attended,total', [(True, 10), (7, None), ('7', 10)])
def test_nonnumeric_attendance_never_creates_a_record(principals, attended, total):
    with pytest.raises(ValueError, match='requires numeric'):
        save_record(principals['faculty'], 1, 1, 'P3', attended, total, 80, 80, 80)
    assert records_for(principals['faculty'], period='P3').empty
    assert administration(principals['admin'])[1].empty
