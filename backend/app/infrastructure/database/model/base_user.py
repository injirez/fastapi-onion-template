from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from infrastructure.database.model.base import Base


class BaseUser(Base):
    """
    Base User model

    Args:
        id (`int`): id
        username (`str`): Username (unique)
        password (`str`): Encrypted password

    To extend user fields use One-To-One relationship
    (https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-one)
    """

    __tablename__ = "base_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

