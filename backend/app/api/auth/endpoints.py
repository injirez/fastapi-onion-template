from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.auth import LoginResponse
from infrastructure.database.engine import sqlalchemy_helper
from repositories.user import SQLAlchemyUserRepository
from services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(sqlalchemy_helper.session_getter),
):
    user_service = AuthService(SQLAlchemyUserRepository(session))
    login_response = await user_service.authenticate_user(form_data)

    return login_response


@router.post("/register", response_model=LoginResponse)
async def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(sqlalchemy_helper.session_getter),
):
    raise NotImplementedError


@router.post("/refresh", response_model=LoginResponse)
async def refresh(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(sqlalchemy_helper.session_getter),
):
    raise NotImplementedError


@router.post("/verify", response_model=LoginResponse)
async def verify(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(sqlalchemy_helper.session_getter),
):
    raise NotImplementedError
