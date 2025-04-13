from typing import List, Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.speciality import Specialty
from src.models.university import University


class UniversityRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_university(self, data: dict) -> University:
        """
        Insert a new university record. 'data' is a dict of fields like:
        {
          "name": "...",
          "image": "...",
          "description": "...",
          ...
        }
        """
        stmt = insert(University).values(**data).returning(University)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def update_university(self, university_id: int, data: dict) -> Optional[University]:
        """
        Update an existing university's fields (by ID). Returns the updated University or None.
        """
        stmt = (
            update(University)
            .where(University.id == university_id)
            .values(**data)
            .returning(University)
        )
        result = await self._session.execute(stmt)
        return result.scalar()

    async def get_university_by_id(self, university_id: int) -> Optional[University]:
        """
        Retrieve a University by its primary key.
        """
        stmt = select(University).where(University.id == university_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_university_by_name(self, name: str) -> Optional[University]:
        """
        Find a University by its unique name.
        """
        stmt = select(University).where(University.name == name)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_university(self, university_id: int) -> None:
        """
        Delete a university by ID. No return value.
        """
        stmt = delete(University).where(University.id == university_id)
        await self._session.execute(stmt)

    async def list_universities(self) -> List[University]:
        """
        List all universities, ordered by creation time descending (if using TimestampMixin).
        """
        stmt = select(University).order_by(University.created_at.desc())
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def list_universities_by_specialty(self, specialty_id: int) -> List[University]:
        """
        Return all universities that offer a given specialty,
        assuming a many-to-many relationship 'University.specialties'.
        """
        stmt = (
            select(University)
            .join(University.specialties)
            .where(Specialty.id == specialty_id)
            .options(joinedload(University.specialties))
            .order_by(University.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_universities_by_country(self, country_name: str) -> list[University]:
        stmt = select(University).where(University.country_name.ilike(country_name))
        result = await self._session.execute(stmt)
        return result.scalars().all()