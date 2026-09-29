# test_app.py - automated tests for the wellbeing app.
# Run them with:  python -m pytest

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # find app.py

import pytest
import database
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    
    monkeypatch.setattr(database, "DB_FILE", str(tmp_path / "test.db"))
    database.create_tables()
    return app_module.app.test_client()


def test_pages_need_login(client):
    response = client.get("/history")
    assert response.status_code == 302                  
    assert "/login" in response.headers["Location"]


def test_sign_up_and_log_in(client):
    client.post("/signup", data={"username": "anna", "password": "sunflower123"})
    assert client.get("/history").status_code == 200  

def test_students_only_see_their_own_check_ins(client):
    client.post("/signup", data={"username": "anna", "password": "sunflower123"})
    client.post("/save", data={"text": "anna secret", "predicted": "sad", "chosen": "sad"})

    client.get("/logout")
    client.post("/signup", data={"username": "ben", "password": "helloworld123"})

    page = client.get("/history").data.decode()
    assert "anna secret" not in page  

def test_api_history(client):
    assert client.get("/api/history").status_code == 401

    client.post("/signup", data={"username": "anna", "password": "sunflower123"})
    client.post("/save", data={"text": "exam tomorrow", "predicted": "worried", "chosen": "worried"})

    data = client.get("/api/history").get_json()
    assert data["checkins"][0]["text"] == "exam tomorrow"

def test_api_checkin_flow(client):
    assert client.get("/api/history").status_code == 401

    client.post("/signup", data={"username": "anna", "password": "sunflower123"})

    response = client.post("/api/checkin", json={"text": "I'm so worried about my exam tomorrow"})
    assert response.get_json()["emotion"] == "worried"

    response = client.post("/api/message", json={"chosen": "worried"})
    assert "worried" in response.get_json()["message"]

    client.post("/api/save", json={"text": "I'm so worried about my exam tomorrow","predicted": "worried", "chosen": "worried"})

    data = client.get("/api/history").get_json()
    assert len(data["checkins"]) == 1