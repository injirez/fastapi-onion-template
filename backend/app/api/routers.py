from fastapi import APIRouter
from api.auth.endpoints import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
