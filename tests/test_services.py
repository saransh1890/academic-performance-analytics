import sqlite3
import time
import pytest
import database
from database import get_conn, init_db, backup_database
from seed_data import seed
from services import *

@pytest.fixture
def setup_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, 'DB_PATH', str(tmp_path / 'test.db'))
    credentials = seed()
    return {name: authenticate(name, password) for name, password in credentials.items()}


def test_authentication_and_password_storage(setup_db):
    assert authenticate('admin', 'wrong') is None
    with get_conn() as conn:
        assert conn.execute('SELECT password_hash FROM users LIMIT 1').fetchone()[0].startswith('pbkdf2_sha256$')
    assert verify_password('a-long-password', password_hash('a-long-password'))
    assert not verify_password('incorrect', password_hash('a-long-password'))


def test_student_privacy_and_write_denial(setup_db):
    p = setup_db['student1']
    assert set(records_for(p).student_id) == {1}
    assert catalog(p)[0].student_id.tolist() == [1]
    with pytest.raises(PermissionError):
        save_record(p, 1,1,'P1',8,10,80,80,80)
    with pytest.raises(PermissionError):
        export_report(p)
    with pytest.raises(PermissionError):
        administration(setup_db['faculty'])
    with pytest.raises(PermissionError):
        records_for(None)


def test_attendance_upsert_and_audit(setup_db):
    p = setup_db['faculty']
    save_record(p,1,1,'P3',3,4,80,80,80)
    save_record(p,1,1,'P3',4,4,90,90,90)
    records = records_for(p,1,'P3')
    assert len(records) == 1
    assert records.iloc[0].attendance_pct == 100
    _, logs = administration(setup_db['admin'])
    assert logs.action.tolist() == ['record.update','record.create']
    assert 'before=' in logs.iloc[0].detail


@pytest.mark.parametrize('values', [(11,10,80,80,80), (0,0,80,80,80), (8,10,-1,80,80), (8,10,float('nan'),80,80), (float('inf'),10,80,80,80)])
def test_invalid_writes_are_atomic(setup_db, values):
    with pytest.raises(ValueError):
        save_record(setup_db['faculty'],1,1,'P3',*values)
    assert records_for(setup_db['faculty'],1,'P3').empty
    assert administration(setup_db['admin'])[1].empty


def test_foreign_keys_and_period_validation(setup_db):
    with pytest.raises(sqlite3.IntegrityError):
        save_record(setup_db['faculty'],999,1,'P3',8,10,80,80,80)
    with pytest.raises(ValueError):
        save_record(setup_db['faculty'],1,1,'October',8,10,80,80,80)


def test_period_aggregation_and_natural_order(setup_db):
    p = setup_db['faculty']
    for subject, value in [(1,40),(2,80)]:
        save_record(p,1,subject,'P10',10,10,value,value,value)
    summary = summarize(records_for(p))
    row = summary[summary['Student ID'] == 1].iloc[0]
    assert row.Period == 'P10'
    assert row.Score == 68  # .8 * average(40,80) + .2 * 100
    assert row.Trend == 'Declining'
    assert summarize(records_for(p), 'P1').iloc[0].Trend == 'No Previous Data'
    assert summarize(records_for(p), 'P9').empty


def test_admin_management_and_revocation(setup_db):
    admin = setup_db['admin']
    save_student(admin,6,'New Student','ECE',3)
    save_subject(admin,3,'NEW','New Subject')
    save_user(admin,'newstudent','secure-password','Student',6)
    new = authenticate('newstudent','secure-password')
    assert records_for(new).empty
    save_user(admin,'newstudent','secure-password','Student',6,False)
    assert authenticate('newstudent','secure-password') is None
    with pytest.raises(PermissionError):
        records_for(new)
    with pytest.raises(ValueError):
        save_user(admin,'admin','secure-password','Faculty')
    with pytest.raises(PermissionError):
        save_student(setup_db['faculty'],7,'Invalid','CSE',1)


def test_seed_idempotency_and_backup(setup_db, tmp_path):
    assert seed() == {}
    assert len(records_for(setup_db['admin'])) == 10
    backup_database(tmp_path / 'backup.db')
    with sqlite3.connect(tmp_path / 'backup.db') as conn:
        assert conn.execute('SELECT count(*) FROM academic_records').fetchone()[0] == 10


def test_report_and_csv_injection(setup_db):
    save_student(setup_db['admin'],1,'=malicious','CSE',5)
    report = export_report(setup_db['faculty'],1,'P1').decode('utf-8-sig')
    assert "'=malicious" in report
    assert 'P2' not in report


def test_lockout(setup_db):
    for _ in range(5):
        assert authenticate('faculty','bad') is None
    with get_conn() as conn:
        assert conn.execute("SELECT failures FROM login_attempts WHERE username='faculty'").fetchone()[0] == 5


def test_normal_load_performance(setup_db):
    start = time.perf_counter()
    for _ in range(20):
        summarize(records_for(setup_db['faculty']))
    assert time.perf_counter() - start < 3
