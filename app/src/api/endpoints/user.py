from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from src.models.user import User_DB, UserRead, UserCreate
from src.database.engine import get_session
from src.common.security import get_password_hash

router = APIRouter()


@router.post("/", response_model=UserRead)
def user_signup(
    user: UserCreate,
    session: Session = Depends(get_session),
) -> Any:
    """
    Insert your data to proceed with signup
    """
    try:
        user.password = get_password_hash(user.password)
        # Inserisci nuovo utente
        db_user = User_DB.from_orm(user)
        session.add(db_user)
        session.commit()
        return db_user
    except Exception:
        print("Impossible to create new user")
        raise HTTPException(status_code=400,
                            detail="Impossible to insert a new user")
