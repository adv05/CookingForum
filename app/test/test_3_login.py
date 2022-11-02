from fastapi.testclient import TestClient
from main import api
from sqlmodel import select
from src.models.user import User_DB
from src.database.engine import get_session_for_sqlmodel

client = TestClient(api)


def test_regular_login():
    response = client.post(
        url="/api/v1/login/",
        data={"username": "Luigi24", "password": "ciaociao"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


def test_regular_login_with_2FA_user():
    response = client.post(
        url="/api/v1/login/",
        data={"username": "Giuseppe80", "password": "super123"}
    )
    response_data = response.json()
    assert response.status_code != 200
    assert "access_token" not in response_data


def test_2FA_login():
    response = client.post(
        url="/api/v1/login/",
        data={"username": "Giuseppe80", "password": "super123"}
    )

    session_user = get_session_for_sqlmodel()
    query = select(User_DB).where(
                User_DB.username == "Giuseppe80")
    user = session_user.exec(query).one()
    assert user.enabled_2FA is True
    assert user.otp is not None
    otpw = user.otp

    response_data = response.json()
    assert response.status_code == 202
    assert "access_token" not in response_data

    response_2FA = client.post(
        url="/api/v1/login/otp-verification/?one_time_pw=" + otpw)
    assert response_2FA.status_code == 200
    response_2FA_data = response_2FA.json()
    assert "access_token" in response_2FA_data
    assert response_2FA_data["token_type"] == "bearer"
    session_user.refresh(user)
    assert getattr(user, 'otp') is None
