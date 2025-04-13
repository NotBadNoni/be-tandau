from typing import List, Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, aliased

from src.models.subject import Subject
from src.models.subject_combination import SubjectCombination


class SubjectCombinationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_subject_combination(self, data: dict) -> SubjectCombination:
        """
        data must have subject1_id, subject2_id, etc.
        """
        stmt = insert(SubjectCombination).values(**data).returning(SubjectCombination)
        res = await self._session.execute(stmt)
        return res.scalar()

    async def update_subject_combination(
            self, combination_id: int, data: dict
    ) -> Optional[SubjectCombination]:
        """
        Update the SubjectCombination row with the given ID using data.
        """
        stmt = (
            update(SubjectCombination)
            .where(SubjectCombination.id == combination_id)
            .values(**data)
            .returning(SubjectCombination)
        )
        res = await self._session.execute(stmt)
        return res.scalar()

    async def get_subject_combination_by_id(
            self, combination_id: int
    ) -> Optional[SubjectCombination]:
        """
        Fetch a single SubjectCombination by its primary key, optionally loading its specialties.
        """
        stmt = (
            select(SubjectCombination)
            .where(SubjectCombination.id == combination_id)
            .options(selectinload(SubjectCombination.specialties))  # eager-load if you have the relationship
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_subjects(self, subject1_id: int, subject2_id: int) -> Optional[SubjectCombination]:
        """
        Fetch the combination that exactly matches the two subject IDs, if it exists.
        """
        stmt = (
            select(SubjectCombination)
            .where(
                SubjectCombination.subject1_id == subject1_id,
                SubjectCombination.subject2_id == subject2_id,
            )
            .options(selectinload(SubjectCombination.specialties))
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_subject_combination(self, combination_id: int) -> None:
        stmt = delete(SubjectCombination).where(SubjectCombination.id == combination_id)
        await self._session.execute(stmt)

    async def list_subject_combinations(self) -> List[dict]:
        """
        Returns a list of subject combinations with full subject1 and subject2 info.
        """
        subject1 = aliased(Subject)
        subject2 = aliased(Subject)

        stmt = (
            select(
                SubjectCombination.id.label("combination_id"),
                subject1.id.label("subject1_id"),
                subject1.name.label("subject1_name"),
                subject2.id.label("subject2_id"),
                subject2.name.label("subject2_name"),
            )
            .join(subject1, SubjectCombination.subject1_id == subject1.id)
            .join(subject2, SubjectCombination.subject2_id == subject2.id)
            .order_by(SubjectCombination.created_at.desc())
        )

        result = await self._session.execute(stmt)

        return [
            {
                "id": row.combination_id,
                "subject1": {
                    "id": row.subject1_id,
                    "name": row.subject1_name,
                },
                "subject2": {
                    "id": row.subject2_id,
                    "name": row.subject2_name,
                }
            }
            for row in result.all()
        ]