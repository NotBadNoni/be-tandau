from typing import List

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.university import University


class UniversityRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_university(self, data: dict) -> University:
        stmt = insert(University).values(**data)
        res = await self._session.execute(stmt)
        return res.scalar()

    async def update_university(self, university_id: int, data: dict) -> University:
        stmt = update(University).values(**data).where(University.id == university_id).returning(University)
        res = await self._session.execute(stmt)
        return res.scalar()

    async def get_university_by_id(self, university_id: int) -> University:
        stmt = select(University).where(University.id == university_id)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_university_by_name(self, name: str) -> University:
        stmt = select(University).where(University.name == name)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_university(self, university_id: int) -> University:
        stmt = delete(University).where(University.id == university_id)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_universities(self) -> List[University]:
        stmt = select(University).order_by(University.created_at.desc())
        res = await self._session.execute(stmt)
        return res.scalars().all()
