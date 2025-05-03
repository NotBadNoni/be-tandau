from typing import List

from src.core.databases import UoW
from src.core.exeptions import NotFoundException
from src.repositories.subject import SubjectRepository
from src.schemas.subject import SubjectResponse


class SubjectController:
    def __init__(self, uow: UoW, subject_repository: SubjectRepository):
        self.uow = uow
        self.subject_repository = subject_repository

    async def list_subjects(self, language: str) -> List[SubjectResponse]:
        subjects = await self.subject_repository.list_subjects()
        return [SubjectResponse.from_model(subject, f"{language}") for subject in subjects]

    async def get_subject(self, subject_id: int, language: str) -> SubjectResponse:
        subject = await self.subject_repository.get_subject_by_id(subject_id)
        if not subject:
            raise NotFoundException("Subject not found.")
        return SubjectResponse.from_model(subject, f"{language}")
