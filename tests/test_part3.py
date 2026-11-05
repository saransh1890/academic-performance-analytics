"""Part 3 boundary, recovery and security regression scenarios."""
import sqlite3
import pytest
import database
import services
from analytics import performance_score, trend_status, intervention_status
from seed_data import seed


@pytest.fixture
def seeded(tmp_path, monkeypatch):
    monkeypatch.setattr(database, 'DB_PATH', str(tmp_path / 'part3.db'))
    passwords = seed()
    return passwords, services.authenticate('admin', passwords['admin'])


@pytest.mark.parametrize('inputs,expected', [((100,0,0,0),40), ((0,100,0,0),25),
    ((0,0,100,0),20), ((0,0,0,100),15), ((0,0,0,0),0), ((100,100,100,100),100)])
def test_independent_weights_and_boundaries(inputs, expected):
    assert performance_score(*inputs) == expected


@pytest.mark.parametrize('value', [-0.01,100.01,float('inf'),float('-inf'),float('nan'),'80',None])
def test_nonfinite_and_invalid_scores(value):
    with pytest.raises(ValueError):
        performance_score(value,80,80,80)


@pytest.mark.parametrize('previous,latest,expected', [(None,80,'No Previous Data'),
    (60,70,'Improving'), (70,60,'Declining'), (70,60.01,'Stable'), (60,69.99,'Stable')])
def test_exact_trend_thresholds(previous, latest, expected):
    assert trend_status(previous, latest) == expected


def test_exact_intervention_thresholds_and_combined_reasons():
    assert intervention_status(50,75,'Stable') == ('Normal', [])
    status,reasons = intervention_status(49.99,74.99,'Declining')
    assert status == 'Needs Intervention'
    assert reasons == ['Low performance score','Low attendance','Declining performance']


def test_password_and_profile_validation(seeded):
    _, admin = seeded
    with pytest.raises(ValueError):
        services.password_hash('short')
    assert not services.verify_password('anything','malformed')
    for sid,semester in [(0,1),(6,0),(6,13)]:
        with pytest.raises(ValueError):
            services.save_student(admin,sid,'Test','CSE',semester)
    for code,name in [('', 'Subject'),('CODE', 'x'*121)]:
        with pytest.raises(ValueError):
            services.save_subject(admin,3,code,name)
    with pytest.raises(ValueError):
        services.save_subject(admin,0,'CODE','Subject')
    for role,sid in [('Unknown',None),('Student',None)]:
        with pytest.raises(ValueError):
            services.save_user(admin,'invalid','test-password',role,sid)


def test_lockout_blocks_correct_password_then_expires(seeded, monkeypatch):
    passwords,_ = seeded
    now = services.time.time()
    monkeypatch.setattr(services.time,'time',lambda: now)
    for _ in range(5):
        assert services.authenticate('faculty','incorrect') is None
    assert services.authenticate('faculty',passwords['faculty']) is None
    monkeypatch.setattr(services.time,'time',lambda: now + 301)
    assert services.authenticate('faculty',passwords['faculty']) is not None
    with database.get_conn() as conn:
        assert conn.execute("SELECT * FROM login_attempts WHERE username='faculty'").fetchone() is None


def test_backup_restore_and_rollback(seeded, tmp_path):
    _,admin = seeded
    with pytest.raises(ValueError):
        database.backup_database(database.DB_PATH)
    destination = tmp_path / 'backups' / 'release.db'
    database.backup_database(destination)
    services.save_student(admin,6,'After backup','CSE',1)
    # Recover the snapshot into a fresh file without touching live data.
    restored = tmp_path / 'restored.db'
    with sqlite3.connect(destination) as source, sqlite3.connect(restored) as target:
        source.backup(target)
        assert target.execute('SELECT count(*) FROM students').fetchone()[0] == 5
        assert target.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert len(services.catalog(admin)[0]) == 6
    with pytest.raises(RuntimeError):
        with database.get_conn() as conn:
            conn.execute("INSERT INTO students VALUES(7,'Rollback','CSE',1)")
            raise RuntimeError('Simulated write failure')
    assert 7 not in services.catalog(admin)[0].student_id.tolist()


def test_old_duplicate_seed_migration(seeded):
    _,admin = seeded
    with database.get_conn() as conn:
        conn.execute('DROP INDEX record_key')
        conn.execute('''INSERT INTO academic_records(student_id,subject_id,period,attendance_pct,
          assignment_score,internal_score,exam_score) VALUES(1,1,'P1',99,99,99,99)''')
    database.init_db()
    data=services.records_for(admin,1,'P1')
    own=data[data.student_id == 1]
    assert len(own) == 1
    assert own.iloc[0].exam_score == 99
    with database.get_conn() as conn, pytest.raises(sqlite3.IntegrityError):
        conn.execute('''INSERT INTO academic_records(student_id,subject_id,period,attendance_pct,
          assignment_score,internal_score,exam_score) VALUES(1,1,'P1',80,80,80,80)''')
