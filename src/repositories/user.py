from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, user: dict) -> User:
        stmt = insert(User).values(**user)
        res = await self._session.execute(stmt)
        return res.scalar()

    async def update_user(self, user_id: int, user: dict) -> User:
        stmt = update(User).values(**user).where(User.id == user_id)
        res = await self._session.execute(stmt)
        return res.scalar()

    async def get_user_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        print(stmt)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()
