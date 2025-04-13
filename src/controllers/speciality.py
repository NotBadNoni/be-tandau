from typing import List

from src.core.databases import UoW
from src.core.exeptions import NotFoundException, BadRequestException
from src.models.speciality import Specialty
from src.repositories.speciality import SpecialtyRepository
from src.repositories.subject_combination import SubjectCombinationRepository


class SpecialtyController:
    def __init__(
            self,
            uow: UoW,
            specialty_repository: SpecialtyRepository,
            subject_combination_repository: SubjectCombinationRepository = None,
    ):
        """
        subject_combination_repository is only needed if you want the 'get_specialties_by_subjects' flow.
        """
        self.uow = uow
        self.specialty_repository = specialty_repository
        self.subject_combination_repository = subject_combination_repository

    async def list_specialties(self) -> List[Specialty]:
        return await self.specialty_repository.list_specialties()

    async def create_specialty(self, data: dict) -> Specialty:
        """
        data might be { "name": "...", "description": "..." }
        """
        async with self.uow:
            existing = await self.specialty_repository.get_specialty_by_name(data["name"])
            if existing:
                raise BadRequestException("Specialty with this name already exists")
            return await self.specialty_repository.create_specialty(data)

    async def get_specialty(self, specialty_id: int) -> Specialty:
        spec = await self.specialty_repository.get_specialty_by_id(specialty_id)
        if not spec:
            raise NotFoundException("Specialty not found")
        return spec

    async def update_specialty(self, specialty_id: int, data: dict) -> Specialty:
        async with self.uow:
            spec = await self.specialty_repository.get_specialty_by_id(specialty_id)
            if not spec:
                raise NotFoundException("Specialty not found")
            if "name" in data:
                same = await self.specialty_repository.get_specialty_by_name(data["name"])
                if same and same.id != specialty_id:
                    raise BadRequestException("Another specialty already has that name")

            return await self.specialty_repository.update_specialty(specialty_id, data)

    async def delete_specialty(self, specialty_id: int):
        async with self.uow:
            spec = await self.specialty_repository.get_specialty_by_id(specialty_id)
            if not spec:
                raise NotFoundException("Specialty not found")
            await self.specialty_repository.delete_specialty(specialty_id)
            return {"detail": "Specialty deleted"}

    async def get_specialties_by_subjects(self, subject1_id: int, subject2_id: int) -> List[Specialty]:
        """
        Returns all specialties for a given combination of subject1_id, subject2_id.
        This requires a many-to-many relationship between SubjectCombination and Specialty.
        """
        if not self.subject_combination_repository:
            raise BadRequestException("SubjectCombinationRepository not provided.")

        combo = await self.subject_combination_repository.get_by_subjects(subject1_id, subject2_id)
        if not combo:
            raise NotFoundException(f"No combination found for subjects {subject1_id} & {subject2_id}.")

        return combo.specialties
