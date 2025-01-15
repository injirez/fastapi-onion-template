from pydantic import BaseModel, field_validator, model_validator

from services.validators import password_complexity_validator


class RefreshToken(BaseModel):
    refresh_token: str


class TokenPair(RefreshToken):
    access_token: str


class Username(BaseModel):
    username: str


class Registration(Username):
    password: str
    repeat_password: str

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        return password_complexity_validator(value)

    @model_validator(mode="after")
    @classmethod
    def passwords_match(cls, values: ["Registration"]) -> dict:
        if values.password != values.repeat_password:
            raise ValueError("Passwords do not match")
        return values
