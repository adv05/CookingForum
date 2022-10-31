from fastapi import APIRouter
from src.api.endpoints import user, login


api_router = APIRouter()

# endpoint per user
api_router.include_router(user.router,
                          prefix="/signup",
                          tags=["signup"]
                          )

# endpoint per il login
api_router.include_router(login.router,
                          prefix="/login",
                          tags=["login"]
                          )
