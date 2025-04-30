from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, aliased

from src.models.subject import Subject
from src.models.subject_combination import SubjectCombination


class SubjectCombinationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_subject_combination_by_id(
            self, combination_id: int
    ) -> Optional[SubjectCombination]:
        stmt = (
            select(SubjectCombination)
            .where(SubjectCombination.id == combination_id)
            .options(selectinload(SubjectCombination.specialties))
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_subjects(self, subject1_id: int, subject2_id: int) -> Optional[SubjectCombination]:
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

    async def list_subject_combinations(self, lang: str = "en") -> List[dict]:
        subject1 = aliased(Subject)
        subject2 = aliased(Subject)

        name1_col = getattr(subject1, f"name_{lang}", subject1.name_en)
        name2_col = getattr(subject2, f"name_{lang}", subject2.name_en)

        stmt = (
            select(
                SubjectCombination.id.label("combination_id"),
                subject1.id.label("subject1_id"),
                name1_col.label("subject1_name"),
                subject2.id.label("subject2_id"),
                name2_col.label("subject2_name"),
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
