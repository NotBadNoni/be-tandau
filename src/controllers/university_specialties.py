from src.core.databases import UoW
from src.core.exeptions import NotFoundException, BadRequestException
from src.repositories.speciality import SpecialtyRepository
from src.repositories.university import UniversityRepository
from src.repositories.university_specialties import UniversitySpecialtiesRepository


class UniversitySpecialtiesController:
    def __init__(
            self,
            uow: UoW,
            university_specialties_repository: UniversitySpecialtiesRepository,
            university_repository: UniversityRepository,
            specialty_repository: SpecialtyRepository
    ):
        self.uow = uow
        self.link_repo = university_specialties_repository
        self.university_repo = university_repository
        self.specialty_repo = specialty_repository

    async def add_specialty_to_university(self, university_id: int, specialty_id: int):
        async with self.uow:
            uni = await self.university_repo.get_university_by_id(university_id)
            if not uni:
                raise NotFoundException("University not found")

            spec = await self.specialty_repo.get_specialty_by_id(specialty_id)
            if not spec:
                raise NotFoundException("Specialty not found")

            link_exists = await self.link_repo.check_link_exists(university_id, specialty_id)
            if link_exists:
                raise BadRequestException("This university is already linked to that specialty")

            await self.link_repo.link_university_to_specialty(university_id, specialty_id)

        return {"detail": "Specialty linked to university successfully"}

    async def remove_specialty_from_university(self, university_id: int, specialty_id: int):
        async with self.uow:
            link_exists = await self.link_repo.check_link_exists(university_id, specialty_id)
            if not link_exists:
                raise NotFoundException("No link found between that university and specialty")

            await self.link_repo.unlink_university_from_specialty(university_id, specialty_id)

        return {"detail": "Link removed successfully"}
