from typing import List, Optional
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.subject import Subject

class SubjectRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_subject(self, data: dict) -> Subject:
        """
        data might look like: {"name": "Math"}
        """
        stmt = insert(Subject).values(**data).returning(Subject)
        res = await self._session.execute(stmt)
        return res.scalar()

    async def update_subject(self, subject_id: int, data: dict) -> Optional[Subject]:
        """
        Update an existing subject by its primary key.
        """
        stmt = (
            update(Subject)
            .where(Subject.id == subject_id)
            .values(**data)
            .returning(Subject)
        )
        res = await self._session.execute(stmt)
        return res.scalar()

    async def get_subject_by_id(self, subject_id: int) -> Optional[Subject]:
        """
        Get a subject record by ID.
        """
        stmt = select(Subject).where(Subject.id == subject_id)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_subject_by_name(self, name: str) -> Optional[Subject]:
        """
        Get a subject by its unique name.
        """
        stmt = select(Subject).where(Subject.name == name)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_subject(self, subject_id: int) -> None:
        stmt = delete(Subject).where(Subject.id == subject_id)
        await self._session.execute(stmt)

    async def list_subjects(self) -> List[Subject]:
        """
        List all subjects, ordered by creation date desc (if using TimestampMixin).
        """
        stmt = select(Subject).order_by(Subject.created_at.desc())
        res = await self._session.execute(stmt)
        return res.scalars().all()
