from src.core.databases import UoW
from src.core.exeptions import NotFoundException
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

    async def get_universities(self, language: str = 'en'):
        universities = await self.university_repository.list_universities()
        return [
            UniversityResponse.from_model(university, f"{language}")
            for university in universities
        ]

    async def get_university(self, university_id: int, language: str = 'en'):
        university = await self.university_repository.get_university_by_id(university_id)
        if not university:
            raise NotFoundException("University not found")
        return UniversityResponse.from_model(university, lang=f"{language}")

    async def get_universities_by_specialty(self, specialty_id: int, language: str = 'en'):
        universities = await self.university_repository.list_universities_by_specialty(specialty_id)
        return [
            UniversityResponse.from_model(university, f"{language}")
            for university in universities
        ]

    async def get_universities_by_country(self, country_name: str, language: str = 'en'):
        universities = await self.university_repository.get_universities_by_country(country_name)
        return [
            UniversityResponse.from_model(university, f"{language}")
            for university in universities
        ]
