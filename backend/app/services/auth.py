from datetime import timedelta, datetime, timezone
from typing import Any

import jwt
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core.settings import settings
from domain.models.auth import LoginResponse
from repositories.user import SQLAlchemyUserRepository
from services.encrypt_decrypt import decrypt


class AuthService:
    __slots__ = ("repository",)

    def __init__(self, repository: SQLAlchemyUserRepository) -> None:
        self.repository = repository

    async def authenticate_user(self, data: OAuth2PasswordRequestForm) -> LoginResponse:
        user = await self.repository.get_by_username(data.username)
        if user is None:
            raise self.__error()

        self.__check_password(data.password, user.password)

        access_token = self.__create_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_EXPIRATION_SECONDS),
        )

        refresh_token = self.__create_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_EXPIRATION_SECONDS),
        )

        return LoginResponse(access_token=access_token, refresh_token=refresh_token, username=user.username)

    def __check_password(self, password: str, db_password: str) -> None:
        if not password == decrypt(db_password):
            raise self.__error()

    @staticmethod
    def __create_token(
            data: dict[str, Any], expires_delta: timedelta
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def __error(
            detail: str = "Incorrect username or password",
            status_code: int = status.HTTP_401_UNAUTHORIZED,
            **kwargs
    ) -> HTTPException:
        return HTTPException(detail=detail, status_code=status_code, **kwargs)
