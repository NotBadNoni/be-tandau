from src.core.databases import UoW
from src.core.exeptions import BadRequestException
from src.repositories.user import UserRepository


class UserController:
    def __init__(
            self,
            uow: UoW,
            user_repository: UserRepository,
    ):
        self.uow = uow
        self.user_repository = user_repository

    async def profile_user(self, user_id: int):
        db_user = await self.user_repository.get_user_by_id(user_id)
        if not db_user:
            raise BadRequestException("User with this id does not exist")

        return db_user
