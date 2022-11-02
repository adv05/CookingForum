from sqlmodel import select
from src.common.security import verify_password
from src.database.engine import get_session_for_sqlmodel
from src.models.user import User_DB
from fastapi.testclient import TestClient
from main import api

client = TestClient(api)


def test_insert_user_in_db():
    new_user = {
        "username": "Piero41",
        "email": "piero41@protonmail.com",
        "name": "Piero",
        "last_name": "Bianchi",
        "password": "asdf789",
        "enabled_2FA": True
    }
    response = client.post("/api/v1/signup/", json=new_user)
    assert response.status_code == 200
    # usr = response.json()

    session_user = get_session_for_sqlmodel()
    query = select(User_DB).where(
                User_DB.username == new_user["username"])
    usr_in_db = session_user.exec(query).one()
    assert usr_in_db.id >= 1
    assert verify_password(new_user["password"], usr_in_db.password)


def test_get_all_users_in_db():
    session_user = get_session_for_sqlmodel()
    query = select(User_DB)
    usr_in_db = session_user.exec(query)
    counter = 0
    for rows in usr_in_db:
        counter += 1
        print(rows)
    assert counter >= 3
    assert usr_in_db
