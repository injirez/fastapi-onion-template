from pydantic import BaseModel


class LoginResponse(BaseModel):
    access_token: str
    username: str


class TokenData(BaseModel):
    username: str
