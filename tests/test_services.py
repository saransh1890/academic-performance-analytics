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




















def test_lockout(setup_db):
    for _ in range(5):
        assert authenticate('faculty','bad') is None
    with get_conn() as conn:
        assert conn.execute("SELECT failures FROM login_attempts WHERE username='faculty'").fetchone()[0] == 5


