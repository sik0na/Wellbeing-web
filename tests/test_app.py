import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # find app.py

import pytest
import database
import app as app_module
import translations
import content
from datetime import datetime

@pytest.fixture
def client(tmp_path, monkeypatch):
    
    monkeypatch.setattr(database, "DB_FILE", str(tmp_path / "test.db"))
    database.create_tables()
    return app_module.app.test_client()


def test_api_needs_login(client):
    assert client.get("/api/history").status_code == 401
    assert client.get("/api/emotions").status_code == 401
    assert client.post("/api/checkin", json={"text": "hello"}).status_code == 401
    assert client.post("/api/save", json={"text": "x", "predicted": "sad", "chosen": "sad"}).status_code == 401


def test_students_only_see_their_own_check_ins(client):
    client.post("/api/signup", json={"username": "anna", "password": "sunflower123"})
    client.post("/api/save", json={"text": "anna secret", "predicted": "sad", "chosen": "sad"})

    client.post("/api/logout")
    client.post("/api/signup", json={"username": "ben", "password": "helloworld123"})

    data = client.get("/api/history").get_json()
    assert data["checkins"] == []                        # Ben sees nothing of Anna's


def test_api_history(client):
    client.post("/api/signup", json={"username": "anna", "password": "sunflower123"})
    client.post("/api/save", json={"text": "exam tomorrow", "predicted": "worried", "chosen": "worried"})

    data = client.get("/api/history").get_json()
    assert data["checkins"][0]["text"] == "exam tomorrow"

def test_api_checkin_flow(client):
    client.post("/api/signup", json={"username": "anna", "password": "sunflower123"})

    response = client.post("/api/checkin", json={"text": "I'm so worried about my exam tomorrow"})
    assert response.get_json()["emotion"] == "worried"

    response = client.post("/api/message", json={"chosen": "worried"})
    assert "worried" in response.get_json()["message"]

    client.post("/api/save", json={"text": "I'm so worried about my exam tomorrow","predicted": "worried", "chosen": "worried"})

    data = client.get("/api/history").get_json()
    assert len(data["checkins"]) == 1

def test_api_login(client):
    response = client.get("/api/me")
    assert response.get_json()["logged_in"] == False
    client.post("/api/signup", json={"username": "anna", "password":"sunflower123"})

    response = client.get("/api/me")
    assert response.get_json()["logged_in"] == True

    client.post("/api/logout")
    response = client.get("/api/me")
    assert response.get_json()["logged_in"] == False

    response= client.post("/api/login", json={"username":"anna", "password":"sunflo3"})
    assert response.status_code == 401

    response = client.post("/api/login", json = {"username":"anna", "password":"sunflower123"})
    assert response.status_code==200

def test_api_emotions(client):
    assert client.get("/api/emotions").status_code == 401
    client.post("/api/signup", json = {"username":"anna", "password":"sunflower123"})
    data = client.get("/api/emotions").get_json()

    keys = [emotion["key"] for emotion in data["emotions"]]
    assert len(keys) == 7
    assert "worried" in keys
    assert data["emotions"][0]["emoji"] == "😟"

def test_translations(client):
    data= client.get("/api/translations/hu").get_json()
    assert data["texts"]["Log in"] == "Bejelentkezés"

    data= client.get("/api/translations/en").get_json()
    assert data["texts"] == {}

    assert client.get("/api/translations/xx").status_code == 404

def test_every_row_has_three_languages():
    for row in translations.ROWS:
        assert len(row) == 3
        for text in row:
            assert text.strip() != ""

def test_messages_in_the_students_language(client):
    client.post("/api/signup", json = {"username":"anna", "password":"sunflower123"})
    data = client.post("/api/message", json = {"chosen": "worried", "lang": "hu"}).get_json()
    assert data["message"].startswith("Érthető")

    data = client.get("/api/emotions?lang=mn").get_json()
    assert data["emotions"][0]["name"] == "Айдас / санаа зоволт"

    data = client.post("/api/message", json = {"chosen": "worried"}).get_json()
    assert "worried" in data["message"]

def test_every_emotion_is_translated():
    for emotion in content.EMOTIONS.values():
        for lang in ["hu", "mn"]:
            assert emotion["name"] in translations.TRANSLATIONS[lang]
            assert emotion["message"] in translations.TRANSLATIONS[lang]

    
def test_api_calendar(client):
    assert client.get("/api/calendar/2026/10").status_code == 401

    client.post("/api/signup", json = {"username":"anna", "password": "sunflower123"})
    client.post("/api/save", json = {"text": "exam soon", "predicted": "worried", "chosen": "worried"})
    client.post("/api/save", json = {"text": "better now", "predicted": "calm", "chosen": "calm"})

    today = datetime.now()
    data = client.get(f"/api/calendar/{today.year}/{today.month}").get_json()
    assert len(data["weeks"]) <= 6                      # a month never has more than 6 weeks

    days = [day for week in data["weeks"] for day in week if day is not None]
    assert days[0]["number"]== 1

    todays_box = [day for day in days if day["number"] == today.day][0]
    assert todays_box["emotion"] == "calm"

    assert todays_box["emoji"] == "😌"
    assert client.get("/api/calendar/2026/13").status_code == 400


def test_api_signup_checks(client):
    response = client.post("/api/signup", json={"username": "al", "password": "sunflower123"})
    assert response.status_code == 400                  # username too short

    response = client.post("/api/signup", json={"username": "anna", "password": "short"})
    assert response.status_code == 400                  # password too short

    assert client.post("/api/signup", json={"username": "anna", "password": "sunflower123"}).status_code == 200
    client.post("/api/logout")
    response = client.post("/api/signup", json={"username": "anna", "password": "sunflower123"})
    assert response.status_code == 400                  # username taken


def test_unknown_api_address_gives_json_404(client):
    response = client.get("/api/nothing-here")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Not found."


def test_react_app_is_served(client):
    if not os.path.exists(os.path.join(app_module.REACT_FOLDER, "index.html")):
        pytest.skip("run 'npm run build' in frontend/ first")
    for address in ["/", "/some/page"]:                 # every page address gets the React app
        response = client.get(address)
        assert response.status_code == 200
        assert b'<div id="root">' in response.data
