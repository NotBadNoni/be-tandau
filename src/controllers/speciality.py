from typing import List

from src.core.databases import UoW
from src.core.exeptions import NotFoundException, BadRequestException
from src.repositories.speciality import SpecialtyRepository
from src.repositories.subject_combination import SubjectCombinationRepository
from src.schemas.specialty import SpecialtyResponse


class SpecialtyController:
    def __init__(
            self,
            uow: UoW,
            specialty_repository: SpecialtyRepository,
            subject_combination_repository: SubjectCombinationRepository = None,
    ):
        self.uow = uow
        self.specialty_repository = specialty_repository
        self.subject_combination_repository = subject_combination_repository

    async def list_specialties(self, language: str) -> List[SpecialtyResponse]:
        specialties = await self.specialty_repository.list_specialties()
        return [SpecialtyResponse.from_model(spec, language) for spec in specialties]

    async def get_specialty(self, specialty_id: int, language: str) -> SpecialtyResponse:
        spec = await self.specialty_repository.get_specialty_by_id(specialty_id)
        if not spec:
            raise NotFoundException("Specialty not found")
        return SpecialtyResponse.from_model(spec, language)

    async def get_specialties_by_subjects(self, subject1_id: int, subject2_id: int, language: str) -> List[
        SpecialtyResponse]:
        if not self.subject_combination_repository:
            raise BadRequestException("SubjectCombinationRepository not provided.")

        combo = await self.subject_combination_repository.get_by_subjects(subject1_id, subject2_id)
        if not combo:
            raise NotFoundException(f"No combination found for subjects {subject1_id} & {subject2_id}.")

        return [SpecialtyResponse.from_model(spec, language) for spec in combo.specialties]
