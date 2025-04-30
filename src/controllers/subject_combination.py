from src.core.databases import UoW
from src.core.exeptions import NotFoundException
from src.models.subject_combination import SubjectCombination
from src.repositories.subject_combination import SubjectCombinationRepository


class SubjectCombinationController:
    def __init__(self, uow: UoW, subject_combination_repository: SubjectCombinationRepository):
        self.uow = uow
        self.subject_combination_repository = subject_combination_repository

    async def list_combinations(self, lang: str = "en") -> list[dict]:
        return await self.subject_combination_repository.list_subject_combinations(lang)

    async def get_combination(self, combination_id: int) -> SubjectCombination:
        combo = await self.subject_combination_repository.get_subject_combination_by_id(combination_id)
        if not combo:
            raise NotFoundException("SubjectCombination not found.")
        return combo
