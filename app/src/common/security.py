from datetime import datetime, timedelta
import random
import string
from typing import Any, Optional, Union
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from src.config import API_STRING, SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
from src.config import ENCODING_ALGORITHM, ENCODE_TOKEN_KEY
from src.models.user import User_DB

reusable_oauth2 = OAuth2PasswordBearer(
                    tokenUrl=f"{API_STRING}/login"
                    )

# Per cryptare la password si crea questo oggetto
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Metodo di CryptContext che hasha la password
# In teoria per la prima volta che l'utente immette la pw
# Quindi si hasha e poi si conserva nel db
def get_password_hash(password: str) -> str:
    return password_context.hash(password)


# Per verificare che la password immessa coincide con quella hashata
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


# Verificare che un utente esista
def verify_user_by_username(
    db: Session,
    usr: str,
    pwd: str
) -> Optional[User_DB]:
    user = db.query(User_DB).filter(User_DB.username == usr).first()
    if not user or not verify_password(pwd, user.password):
        print("Utente non esistente o password sbagliata")
        return None
    return user


def check_2FA_enabled(
    db: Session,
    usr: str
) -> bool:
    user = db.query(User_DB).filter(User_DB.username == usr).first()
    if user.enabled_2FA is True:
        return True
    else:
        return False


# crea un token per user
def create_access_token(
    string_item: Union[str, Any], expires_delta: timedelta = None
) -> str:
    # Controlla che il token non sia scaduto
    if expires_delta:  # se c'era scadenza la mantiene, altrimenti
        #               gliene assegna una nuova con l'else
        # expiration_date è un tipo data
        expiration_date = datetime.utcnow() + expires_delta
    else:
        # timedelta restituisce il valore dato in formato data
        expiration_date = datetime.utcnow() + timedelta(
            minutes=SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
            )
    # Genera un token partendo da data scadenza, idUtente e chiave di sic
    to_encode = {"exp": expiration_date, "sub": str(string_item)}
    encoded_jwt = jwt.encode(
        to_encode, ENCODE_TOKEN_KEY, algorithm=ENCODING_ALGORITHM
    )
    return encoded_jwt


def create_token_response(usr: User_DB) -> Any:
    access_token_expires = timedelta(
            minutes=SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            usr.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }


# Genera one time password
def generate_random_otp() -> str:
    rand = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10
            ))
    return rand
