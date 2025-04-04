from typing import List, Optional

from src.core.databases import UoW
from src.core.exeptions import BadRequestException, NotFoundException
from src.repositories.university import UniversityRepository
from src.schemas.university import UniversityResponse


class UniversityController:
    def __init__(
        self,
        uow: UoW,
        university_repository: UniversityRepository,
    ):
        self.uow = uow
        self.university_repository = university_repository

    async def get_universities(self) -> List[UniversityResponse]:
        universities = await self.university_repository.list_universities()
        return [UniversityResponse.model_validate(u) for u in universities]

    async def get_university(self, university_id: int) -> UniversityResponse:
        university = await self.university_repository.get_university_by_id(university_id)
        if not university:
            raise NotFoundException("University not found")
        return UniversityResponse.model_validate(university)

    async def create_university(self, data: dict) -> UniversityResponse:
        async with self.uow:
            db_university = await self.university_repository.get_university_by_name(data['name'])
            if db_university:
                raise BadRequestException("University already exists")

            university = await self.university_repository.create_university(data)
            return UniversityResponse.model_validate(university)

    async def update_university(self, university_id: int, data: dict) -> dict:
        async with self.uow:
            db_university = await self.university_repository.get_university_by_id(university_id)
            if not db_university:
                raise NotFoundException("University with this id does not exist")

            await self.university_repository.update_university(university_id, data)
            return {"detail": "University updated successfully"}

    async def delete_university(self, university_id: int) -> dict:
        async with self.uow:
            db_university = await self.university_repository.get_university_by_id(university_id)
            if not db_university:
                raise NotFoundException("University with this id does not exist")

            await self.university_repository.delete_university(university_id)
            return {"detail": "University deleted successfully"}
