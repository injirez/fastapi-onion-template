from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import NoReturn

from infrastructure.database.model.base_user import BaseUser


class SQLAlchemyUserRepository:
    """A repository to work with user db model"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_username(self, username: str) -> BaseUser | None:
        result = await self.session.execute(
            select(BaseUser).filter(BaseUser.username == username)
        )
        return result.scalars().first()

    async def create(self, **kwargs) -> BaseUser:
        result = await self.session.execute(
            insert(BaseUser).values(**kwargs).returning(BaseUser)
        )
        return result.scalars().first()

    async def update(self, base_user: BaseUser, **kwargs) -> NoReturn:
        return NotImplementedError

    async def delete(self, base_user: BaseUser, **kwargs) -> NoReturn:
        return NotImplementedError
