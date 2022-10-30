import fastapi
import uvicorn
from sqlmodel import select
from app.src.database.engine import create_table
from app.src.api.api import api_router
from app.src.config import API_STRING, PROJECT_NAME
# from app.src.config import API_ENDPOINT_HOST, API_ENDPOINT_PORT
from app.src.models.user import User_DB
from app.src.database.engine import insert_data, get_session_for_sqlmodel
from app.src.common.security import get_password_hash


api = fastapi.FastAPI(
    title=PROJECT_NAME,
    openapi_url=f"{API_STRING}/openapi.json",
    # con questa linea tutto deve essere autenticato prima
    # dependencies=[Depends(api(token))]
)

api.include_router(api_router, prefix=API_STRING)  # da togliere


@api.on_event("startup")
def on_startup():
    create_table()

    # Create the admin user
    admin_user = User_DB(
        username="admin",
        email="admin@cookingforum.com",
        hashed_pw=get_password_hash("dummy"),
        isAdmin=True
    )
    # Check if already exists
    session = get_session_for_sqlmodel()
    query = select(User_DB).where(User_DB.username == admin_user.username)
    check_user = session.exec(query).first()
    if check_user:
        print("User already exist, not inserted")
    else:
        # Insert the admin user
        insert_data(admin_user)
        print("Admin user inserted")


if __name__ == "__main__":
    uvicorn.run(api, port="8000", host="127.0.0.1")
