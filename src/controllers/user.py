from src.core.databases import UoW
from src.core.exeptions import BadRequestException
from src.repositories.user import UserRepository
from src.schemas.user import UserUpdate
from src.services.password import PasswordHandler


class UserController:
    def __init__(
            self,
            uow: UoW,
            user_repository: UserRepository,
            password_service: PasswordHandler
    ):
        self.uow = uow
        self.user_repository = user_repository
        self.password_service = password_service

    async def profile_user(self, user_id: int):
        db_user = await self.user_repository.get_user_by_id(user_id)
        if not db_user:
            raise BadRequestException("User with this id does not exist")

        return db_user

    async def profile_change(self, user_id: int, form: UserUpdate):
        db_user = await self.user_repository.get_user_by_id(user_id)
        if not db_user:
            raise BadRequestException("User not found")

        if db_user.username != form.username:
            if await self.user_repository.get_user_by_username(form.username):
                raise BadRequestException("User with this username already exists")
        if db_user.email != form.email:
            if await self.user_repository.get_user_by_email(form.email):
                raise BadRequestException("User with this email already exists")
        update_data = form.dict(exclude_unset=True)
        async with self.uow:
            await self.user_repository.update_user(db_user.id, update_data)

            if form.password:
                if not form.new_password or not form.verify_new_password:
                    raise BadRequestException("New Password and Verification are required")

                if not self.password_service.verify(db_user.password, form.password):
                    raise BadRequestException("Current password does not match")

                if form.new_password != form.verify_new_password:
                    raise BadRequestException("New password and verification do not match")

                db_user.password = self.password_service.hash(form.new_password)
                await self.user_repository.update_user(db_user.id, {"password": db_user.password})

        return db_user
