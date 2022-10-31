from datetime import timedelta
from http.client import HTTPException
from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.common.security import create_access_token
from src.config import SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
from src.models.token import Token
from src.common.security import reusable_oauth2
from src.database.engine import get_session
from src.common.security import verify_user_by_username

router = APIRouter()


@router.post("/access-token", response_model=Token)
def login_access_token(
    database: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Login token compatibile con OAuth2
    Ottieni access token"""

    # Verifichiamo che l'utente esista tramite username
    user_access = verify_user_by_username(
        database, username=form_data.username, password=form_data.password
    )

    if not user_access:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")
    access_token_expires = timedelta(
        minutes=SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user_access.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }


# Validazione token
@router.get("/test")
def read_token(token: str = Depends(reusable_oauth2)):
    return {"token": token}
