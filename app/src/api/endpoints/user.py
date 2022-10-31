from http.client import HTTPException
from typing import Any
from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.models.user import User_DB
from src.database.engine import get_session
from src.common.security import get_password_hash
from src.models.user import UserRead, UserCreate


router = APIRouter()


@router.post("/", response_model=UserRead)
def user_signup(
    user: UserCreate,
    session: Session = Depends(get_session),
) -> Any:
    """
    Insert new user
    """
    try:
        user.hashed_pw = get_password_hash(user.hashed_pw)
        # Inserisci nuovo utente
        db_user = User_DB.from_orm(user)
        session.add(db_user)
        session.commit()
        return db_user
    except Exception:
        print("Impossible to create new user")
        raise HTTPException(status_code=400,
                            detail="Impossible to insert a new user")
