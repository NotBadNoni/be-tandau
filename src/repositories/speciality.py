from typing import List, Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.speciality import Specialty


class SpecialtyRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_specialty(self, data: dict) -> Specialty:
        stmt = insert(Specialty).values(**data).returning(Specialty)
        res = await self._session.execute(stmt)
        return res.scalar()

    async def update_specialty(self, specialty_id: int, data: dict) -> Optional[Specialty]:
        stmt = (
            update(Specialty)
            .where(Specialty.id == specialty_id)
            .values(**data)
            .returning(Specialty)
        )
        res = await self._session.execute(stmt)
        return res.scalar()

    async def get_specialty_by_id(self, specialty_id: int) -> Optional[Specialty]:
        stmt = select(Specialty).where(Specialty.id == specialty_id)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_specialty_by_name(self, name: str) -> Optional[Specialty]:
        stmt = select(Specialty).where(Specialty.name == name)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_specialty(self, specialty_id: int) -> None:
        stmt = delete(Specialty).where(Specialty.id == specialty_id)
        await self._session.execute(stmt)

    async def list_specialties(self) -> List[Specialty]:
        stmt = select(Specialty).order_by(Specialty.created_at.desc())
        res = await self._session.execute(stmt)
        return res.scalars().all()
