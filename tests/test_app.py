# test_app.py - automated tests for the wellbeing app.
# Run them with:  python -m pytest

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # find app.py

import pytest
import database
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    """A fake browser, with its own empty database (so tests never touch wellbeing.db)."""
    monkeypatch.setattr(database, "DB_FILE", str(tmp_path / "test.db"))
    database.create_tables()
    return app_module.app.test_client()


def test_pages_need_login(client):
    response = client.get("/history")
    assert response.status_code == 302                  # 302 = redirect
    assert "/login" in response.headers["Location"]


def test_sign_up_and_log_in(client):
    client.post("/signup", data={"username": "anna", "password": "sunflower123"})
    assert client.get("/history").status_code == 200    # logged in now