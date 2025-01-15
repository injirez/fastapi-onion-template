from datetime import timedelta, datetime, timezone
from typing import Any

import jwt
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError

from core.settings import settings
from domain.models.auth import RefreshToken, TokenPair, Username, Registration
from repositories.user import SQLAlchemyUserRepository
from services.encrypt_decrypt import decrypt, encrypt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class AuthService:
    """
    Main authentication service:

    - authenticate_user
    - refresh_token
    - verify_token
    - register
    """
    __slots__ = ("repository",)

    def __init__(self, repository: SQLAlchemyUserRepository) -> None:
        self.repository = repository

    async def authenticate_user(self, data: OAuth2PasswordRequestForm) -> TokenPair:
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
            expires_delta=timedelta(minutes=settings.JWT_REFRESH_EXPIRATION_SECONDS),
        )

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, data: RefreshToken) -> TokenPair:
        payload = self.__verify_token(data.refresh_token)
        user = await self.repository.get_by_username(payload.get("sub"))
        if user is None:
            raise self.__error()

        access_token = self.__create_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_EXPIRATION_SECONDS),
        )

        return TokenPair(access_token=access_token, refresh_token=data.refresh_token)

    async def verify_token(self, token: str) -> Username:
        payload = self.__verify_token(token)
        user = await self.repository.get_by_username(payload.get("sub"))
        if user is None:
            raise self.__error()

        return Username(username=user.username)

    async def register(self, data: Registration) -> TokenPair:
        data.password = encrypt(data.password)
        try:
            user = await self.repository.create(**data.model_dump(exclude={"repeat_password"}))
        except IntegrityError:
            raise self.__error(detail="Username already exist")
        return await self.authenticate_user(
            OAuth2PasswordRequestForm(
                username=user.username, password=data.repeat_password
            )
        )

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

    def __verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except jwt.PyJWTError as e:
            raise self.__error(detail=f"Invalid token: {e}")

    @staticmethod
    def __error(
            detail: str = "Incorrect username or password",
            status_code: int = status.HTTP_401_UNAUTHORIZED,
            **kwargs
    ) -> HTTPException:
        return HTTPException(detail=detail, status_code=status_code, **kwargs)
