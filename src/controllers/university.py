from src.core.databases import UoW
from src.core.exeptions import BadRequestException
from src.repositories.university import UniversityRepository


class UniversityController:
    def __init__(
        self,
        uow: UoW,
        university_repository: UniversityRepository,
    ):
        self.uow = uow
        self.university_repository = university_repository

    async def get_universities(self):
        return await self.university_repository.list_universities()

    async def get_university(self, university_id: int):
        return await self.university_repository.get_university_by_id(university_id)

    async def create_university(self, data: dict):
        async with self.uow:
            db_university = await self.university_repository.get_university_by_name(data['name'])
            if db_university:
                raise BadRequestException("University already exists")

            university = await self.university_repository.create_university(data)
            return university

    async def update_university(self, university_id: int, data: dict):
        async with self.uow:
            db_university = await self.university_repository.get_university_by_id(university_id)
            if not db_university:
                raise BadRequestException("University with this id not exists")

            await self.university_repository.update_university(university_id, data)
            return {"detail": "University updated successfully"}

    async def delete_university(self, university_id: int):
        async with self.uow:
            db_university = await self.university_repository.get_university_by_id(university_id)
            if not db_university:
                raise BadRequestException("University with this id not exists")

            await self.university_repository.delete_university(university_id)
            return {"detail": "University deleted successfully"}
