from pydantic import BaseModel


class BaseUserDb(BaseModel):
    id: int | None = None
    username: str
    password: str
