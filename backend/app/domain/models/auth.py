from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str


class TokenPair(RefreshToken):
    access_token: str


class LoginResponse(TokenPair):
    username: str
