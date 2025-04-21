from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import SubjectCombinationSpecialties


class SubjectCombinationSpecialtiesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def link_subject_combination_to_specialty(self, combination_id: int, specialty_id: int) -> None:
        stmt = insert(SubjectCombinationSpecialties).values(
            subject_combination_id=combination_id,
            specialty_id=specialty_id
        )
        await self._session.execute(stmt)

    async def unlink_subject_combination_from_specialty(self, combination_id: int, specialty_id: int) -> None:
        stmt = delete(SubjectCombinationSpecialties).where(
            SubjectCombinationSpecialties.subject_combination_id == combination_id,
            SubjectCombinationSpecialties.specialty_id == specialty_id
        )
        await self._session.execute(stmt)

    async def check_link_exists(self, combination_id: int, specialty_id: int) -> bool:
        stmt = select(SubjectCombinationSpecialties).where(
            SubjectCombinationSpecialties.subject_combination_id == combination_id,
            SubjectCombinationSpecialties.specialty_id == specialty_id
        )
        result = await self._session.execute(stmt)
        row = result.first()
        return row is not None
