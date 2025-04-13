from src.core.databases import UoW
from src.core.exeptions import NotFoundException, BadRequestException
from src.repositories.speciality import SpecialtyRepository
from src.repositories.subject_combination import SubjectCombinationRepository
from src.repositories.subject_combination_specialties import SubjectCombinationSpecialtiesRepository


class SubjectCombinationSpecialtiesController:
    def __init__(
            self,
            uow: UoW,
            subject_combination_specialties_repository: SubjectCombinationSpecialtiesRepository,
            subject_combination_repository: SubjectCombinationRepository,
            specialty_repository: SpecialtyRepository
    ):
        self.uow = uow
        self.link_repo = subject_combination_specialties_repository
        self.combo_repo = subject_combination_repository
        self.spec_repo = specialty_repository

    async def add_specialty_to_combination(self, combination_id: int, specialty_id: int):
        """
        Creates the link between a SubjectCombination and a Specialty.
        Raises NotFoundException if either doesn't exist.
        Raises BadRequestException if the link already exists.
        """
        async with self.uow:
            combo = await self.combo_repo.get_subject_combination_by_id(combination_id)
            if not combo:
                raise NotFoundException("Subject combination not found")

            spec = await self.spec_repo.get_specialty_by_id(specialty_id)
            if not spec:
                raise NotFoundException("Specialty not found")

            link_exists = await self.link_repo.check_link_exists(combination_id, specialty_id)
            if link_exists:
                raise BadRequestException("This combination is already linked to that specialty")

            await self.link_repo.link_subject_combination_to_specialty(combination_id, specialty_id)

        return {"detail": "Specialty linked to subject combination successfully"}

    async def remove_specialty_from_combination(self, combination_id: int, specialty_id: int):
        """
        Removes the link between a SubjectCombination and a Specialty.
        Raises NotFoundException if no such link exists.
        """
        async with self.uow:
            link_exists = await self.link_repo.check_link_exists(combination_id, specialty_id)
            if not link_exists:
                raise NotFoundException("No link found between that combination and specialty")

            await self.link_repo.unlink_subject_combination_from_specialty(combination_id, specialty_id)

        return {"detail": "Link removed successfully"}
