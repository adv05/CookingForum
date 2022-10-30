from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.src.config import API_STRING


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
