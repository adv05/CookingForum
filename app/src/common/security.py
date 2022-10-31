from datetime import datetime, timedelta
from typing import Any, Optional, Union
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from src.config import API_STRING, SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
from src.config import ENCODING_ALGORITHM, ENCODE_TOKEN_KEY
from src.models.user import User_DB


reusable_oauth2 = OAuth2PasswordBearer(
                    tokenUrl=f"{API_STRING}/login/access-token"
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
    username: str,
    password: str
) -> Optional[User_DB]:
    user = db.query(User_DB).filter(User_DB.username == username).first()
    # if not user:
    #     return None  # da migliorare con or
    # if not verify_password(password, user.hashed_pw):
    #     return None
    if not user or not verify_password(password, user.hashed_pw):
        print("Utente non esistente o password sbagliata")
        return None
    return user


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
