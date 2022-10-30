from fastapi import APIRouter
from app.src.api.endpoints import user


api_router = APIRouter()

# endpoint per user
api_router.include_router(user.router, prefix="/user", tags=["user"])
