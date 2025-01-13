from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.auth import RefreshToken, TokenPair, Username
from infrastructure.database.engine import sqlalchemy_helper
from repositories.user import SQLAlchemyUserRepository
from services.auth import AuthService, oauth2_scheme

router = APIRouter()


@router.post("/login", response_model=TokenPair)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(sqlalchemy_helper.session_getter),
):
    auth_service = AuthService(SQLAlchemyUserRepository(session))
    login_response = await auth_service.authenticate_user(form_data)

    return login_response


@router.post("/register", response_model=TokenPair)
async def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(sqlalchemy_helper.session_getter),
):
    raise NotImplementedError


@router.post("/refresh", response_model=TokenPair)
async def refresh(
    form_data: RefreshToken,
    session: AsyncSession = Depends(sqlalchemy_helper.session_getter),
):
    auth_service = AuthService(SQLAlchemyUserRepository(session))
    token_pair_response = await auth_service.refresh_token(form_data)

    return token_pair_response


@router.post("/verify", response_model=Username)
async def verify(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(sqlalchemy_helper.session_getter),
):
    auth_service = AuthService(SQLAlchemyUserRepository(session))
    token_pair_response = await auth_service.verify_token(token)

    return token_pair_response
