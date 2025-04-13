from typing import List

from src.core.databases import UoW
from src.core.exeptions import NotFoundException, BadRequestException
from src.models.subject import Subject
from src.repositories.subject import SubjectRepository


class SubjectController:
    def __init__(self, uow: UoW, subject_repository: SubjectRepository):
        self.uow = uow
        self.subject_repository = subject_repository

    async def list_subjects(self) -> List[Subject]:
        return await self.subject_repository.list_subjects()

    async def create_subject(self, data: dict) -> Subject:
        """
        data might look like {"name": "Math"}
        """
        async with self.uow:
            # check if there's already a subject with the same name
            existing = await self.subject_repository.get_subject_by_name(data["name"])
            if existing:
                raise BadRequestException("Subject with that name already exists.")
            return await self.subject_repository.create_subject(data)

    async def get_subject(self, subject_id: int) -> Subject:
        subject = await self.subject_repository.get_subject_by_id(subject_id)
        if not subject:
            raise NotFoundException("Subject not found.")
        return subject

    async def update_subject(self, subject_id: int, data: dict) -> Subject:
        """
        data can have fields like {"name": "New Subject Name"}
        """
        async with self.uow:
            # confirm subject exists
            subject = await self.subject_repository.get_subject_by_id(subject_id)
            if not subject:
                raise NotFoundException("Subject not found.")

            # if changing name, check for duplicates
            if "name" in data:
                dup = await self.subject_repository.get_subject_by_name(data["name"])
                if dup and dup.id != subject_id:
                    raise BadRequestException("Another subject already has that name.")

            updated = await self.subject_repository.update_subject(subject_id, data)
            return updated

    async def delete_subject(self, subject_id: int):
        async with self.uow:
            subject = await self.subject_repository.get_subject_by_id(subject_id)
            if not subject:
                raise NotFoundException("Subject not found.")
            await self.subject_repository.delete_subject(subject_id)
            return {"detail": "Subject deleted successfully"}
