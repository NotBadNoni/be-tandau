from typing import Optional
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.profile import Profile

class ProfileRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_profile(self, data: dict) -> Profile:
        stmt = insert(Profile).values(**data).returning(Profile)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def update_profile(self, user_id: int, data: dict) -> Optional[Profile]:
        stmt = (
            update(Profile)
            .where(Profile.user_id == user_id)
            .values(**data)
            .returning(Profile)
        )
        result = await self._session.execute(stmt)
        profile = result.scalar_one_or_none()  # или .scalars().first()
        return profile

    async def get_profile_by_id(self, profile_id: int) -> Optional[Profile]:
        stmt = select(Profile).where(Profile.id == profile_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_profile(self, profile_id: int) -> None:
        stmt = delete(Profile).where(Profile.id == profile_id)
        await self._session.execute(stmt)

    async def get_profile_by_user_id(self, user_id: int) -> Optional[Profile]:
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = await self._session.scalars(stmt)
        return result.first()