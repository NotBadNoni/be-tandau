from typing import List
from src.core.databases import UoW
from src.core.exeptions import NotFoundException, BadRequestException
from src.models.subject_combination import SubjectCombination
from src.repositories.subject_combination import SubjectCombinationRepository

class SubjectCombinationController:
    def __init__(
        self,
        uow: UoW,
        subject_combination_repository: SubjectCombinationRepository
    ):
        self.uow = uow
        self.subject_combination_repository = subject_combination_repository

    async def list_combinations(self) -> list[dict]:
        """
        Returns all subject combinations.
        """
        return await self.subject_combination_repository.list_subject_combinations()

    async def create_combination(self, data: dict) -> SubjectCombination:
        """
        Create a new SubjectCombination. data should have { subject1_id, subject2_id }.
        """
        async with self.uow:
            existing = await self.subject_combination_repository.get_by_subjects(
                data["subject1_id"], data["subject2_id"]
            )
            if existing:
                raise BadRequestException("This combination already exists.")

            new_combo = await self.subject_combination_repository.create_subject_combination(data)
            return new_combo

    async def get_combination(self, combination_id: int) -> SubjectCombination:
        """
        Retrieve a single SubjectCombination by ID.
        """
        combo = await self.subject_combination_repository.get_subject_combination_by_id(combination_id)
        if not combo:
            raise NotFoundException("SubjectCombination not found.")
        return combo

    async def update_combination(self, combination_id: int, data: dict) -> SubjectCombination:
        """
        Update an existing SubjectCombination. data can have subject1_id, subject2_id, etc.
        """
        async with self.uow:
            existing_combo = await self.subject_combination_repository.get_subject_combination_by_id(combination_id)
            if not existing_combo:
                raise NotFoundException("SubjectCombination not found.")

            if "subject1_id" in data and "subject2_id" in data:
                maybe_duplicate = await self.subject_combination_repository.get_by_subjects(
                    data["subject1_id"], data["subject2_id"]
                )
                if maybe_duplicate and maybe_duplicate.id != combination_id:
                    raise BadRequestException("That new combination already exists.")

            updated_combo = await self.subject_combination_repository.update_subject_combination(combination_id, data)
            return updated_combo

    async def delete_combination(self, combination_id: int):
        """
        Delete a SubjectCombination by ID.
        """
        async with self.uow:
            existing_combo = await self.subject_combination_repository.get_subject_combination_by_id(combination_id)
            if not existing_combo:
                raise NotFoundException("SubjectCombination not found.")

            await self.subject_combination_repository.delete_subject_combination(combination_id)
            return {"detail": "SubjectCombination deleted successfully"}
