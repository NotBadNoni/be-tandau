from typing import List, Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, data: dict) -> User:
        stmt = insert(User).values(**data).returning(User)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def update_user(self, user_id: int, data: dict) -> Optional[User]:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**data)
            .returning(User)
        )
        result = await self._session.execute(stmt)
        return result.scalar()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        stmt = (
            select(User)
            .options(selectinload(User.profile))
            .where(User.id == user_id).limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: int) -> None:
        stmt = delete(User).where(User.id == user_id)
        await self._session.execute(stmt)

    async def list_users(self) -> List[User]:
        stmt = select(User).order_by(User.created_at.desc())
        result = await self._session.execute(stmt)
        return result.scalars().all()
