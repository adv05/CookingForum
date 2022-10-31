from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlmodel import select
from src.models.user import User_DB
from src.models.token import Token
from src.common.security import reusable_oauth2, check_2FA_enabled
from src.common.security import create_token_response
from src.common.security import generate_random_otp, verify_user_by_username
from src.database.engine import get_session, get_session_for_sqlmodel

router = APIRouter()


# Gestione login dell'utente
# Se non ha 2FA e user:pass sono corrette, assegna l'access-token
# Se ha abilitato il 2FA, allora genera OTP da usare su /otp-verification
@router.post("/", response_model=Token)
def user_login(
    database: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Login token compatible with OAuth2\n
    Get access token"""

    # Verifichiamo che l'utente esista tramite username
    user_access = verify_user_by_username(
        database, usr=form_data.username, pwd=form_data.password
    )

    if not user_access:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")

    if check_2FA_enabled(database, user_access.username):
        print("User has 2FA set")
        one_time_pw = generate_random_otp()

        session_user = get_session_for_sqlmodel()
        query = select(User_DB).where(
                    User_DB.username == form_data.username)
        result = session_user.exec(query)
        user = result.one()
        user.otp = one_time_pw
        session_user.add(user)
        session_user.commit()
        session_user.refresh(user)

        # Manca implementazione con email reale
        print("Your password was sent to", user_access.email,
              "\n{ This is your one-time password:", one_time_pw, "}")
        raise HTTPException(status_code=202,
                            detail="You have 2FA enabled. A one time password "
                            + "was sent to your email address: "
                            + user_access.email)
    return create_token_response(user_access)


@router.post("/otp-verification", response_model=Token)
def complete_2FA(one_time_pw: str) -> Any:
    """Insert the code you received via email"""

    # Se il codice immesso corrisponde con l'OTP salvato nel DB, allora auth
    try:
        session_user = get_session_for_sqlmodel()
        query = select(User_DB).where(
                    User_DB.otp == one_time_pw)
        result = session_user.exec(query)

        user = result.one()
        setattr(user, 'otp', None)
        session_user.add(user)
        session_user.commit()
        session_user.refresh(user)
        return create_token_response(user)
    except Exception:
        raise HTTPException(status_code=401,
                            detail="Unvalid code")


# USARE NEI TEST
# Validazione token
@router.get("/read-token")
def read_token_of_logged_in_user(token: str = Depends(reusable_oauth2)):
    return {"token": token}
