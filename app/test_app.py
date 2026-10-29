import psycopg2
from unittest.mock import MagicMock

from app import app


def test_home():
    client = app.test_client()
    assert client.get("/").status_code == 200

def test_healthz():
    client = app.test_client()
    assert client.get("/healthz").status_code == 200

def test_readyz_ok_when_db_reachable(monkeypatch):
    monkeypatch.setattr(pscycopg2, "connect", lambda *a, **k: MagicMock())
    client = app.test_client()
    assert client.get("/readyz").status_code == 200

def test_readyz_503_when_db_down(monkeypatch):
    def fail(*a, **k):
        raise psycopg2.OperationalError("db down")
    monkeypatch.setattr(psycopg2, "connect", fail)
    client = app.test_client()
    assert client.get("/readyz").status_code == 503