from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UniversitySpecialties


class UniversitySpecialtiesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def link_university_to_specialty(self, university_id: int, specialty_id: int) -> None:
        """
        Inserts a row (university_id, specialty_id) into the 'university_specialties' table.
        """
        stmt = insert(UniversitySpecialties).values(
            university_id=university_id,
            specialty_id=specialty_id
        )
        await self._session.execute(stmt)

    async def unlink_university_from_specialty(self, university_id: int, specialty_id: int) -> None:
        """
        Deletes the row linking university_id and specialty_id.
        """
        stmt = delete(UniversitySpecialties).where(
            UniversitySpecialties.university_id == university_id,
            UniversitySpecialties.specialty_id == specialty_id
        )
        await self._session.execute(stmt)

    async def check_link_exists(self, university_id: int, specialty_id: int) -> bool:
        """
        Checks if the row (university_id, specialty_id) exists in the 'university_specialties' table.
        """
        stmt = select(UniversitySpecialties).where(
            UniversitySpecialties.university_id == university_id,
            UniversitySpecialties.specialty_id == specialty_id
        )
        result = await self._session.execute(stmt)
        row = result.first()
        return row is not None
