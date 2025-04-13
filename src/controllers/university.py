from src.core.databases import UoW
from src.core.exeptions import NotFoundException, BadRequestException
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
        university = await self.university_repository.get_university_by_id(university_id)
        if not university:
            raise NotFoundException("University not found")
        return university

    async def create_university(self, data: dict):
        async with self.uow:
            existing = await self.university_repository.get_university_by_name(data["name"])
            if existing:
                raise BadRequestException("University already exists")
            created = await self.university_repository.create_university(data)
            return created

    async def update_university(self, university_id: int, data: dict):
        async with self.uow:
            existing = await self.university_repository.get_university_by_id(university_id)
            if not existing:
                raise NotFoundException("University not found")
            updated = await self.university_repository.update_university(university_id, data)
            return updated

    async def delete_university(self, university_id: int):
        async with self.uow:
            existing = await self.university_repository.get_university_by_id(university_id)
            if not existing:
                raise NotFoundException("University not found")
            await self.university_repository.delete_university(university_id)
            return {"detail": "University deleted successfully"}

    async def get_universities_by_specialty(self, specialty_id: int):
        """
        Retrieve all universities offering the specified specialty.
        Assumes your UniversityRepository has a list_universities_by_specialty() method.
        """
        return await self.university_repository.list_universities_by_specialty(specialty_id)

    async def get_universities_by_country(self, country_name: str):
        universities = await self.university_repository.get_universities_by_country(country_name)
        if not universities:
            raise NotFoundException(f"No universities found for country: {country_name}")
        return universities