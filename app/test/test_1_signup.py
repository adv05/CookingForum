from fastapi.testclient import TestClient
from main import api
from src.database.engine import create_table

client = TestClient(api)
create_table()


def test_user_signup():
    new_user = {
        "username": "Luigi24",
        "email": "luigi24@gmail.com",
        "name": "Luigi",
        "last_name": "Verdi",
        "password": "ciaociao",
        "enabled_2FA": False
    }
    response = client.post("/api/v1/signup/", json=new_user)
    assert response.status_code == 200
    usr = response.json()
    assert usr["username"] == new_user["username"]
    assert "id" in usr


def test_user_signup_with_2FA():
    new_user = {
        "username": "Giuseppe80",
        "email": "giuseppe80@hotmail.com",
        "name": "Giuseppe",
        "last_name": "Bianchi",
        "password": "super123",
        "enabled_2FA": True
    }
    response = client.post("/api/v1/signup/", json=new_user)
    assert response.status_code == 200
    usr = response.json()
    assert usr["username"] == new_user["username"]
    assert "id" in usr
    assert usr["enabled_2FA"] is True
