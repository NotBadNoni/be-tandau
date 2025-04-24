from src.core.databases import UoW
from src.core.exeptions import BadRequestException, NotFoundException
from src.repositories.profile import ProfileRepository
from src.repositories.user import UserRepository
from src.schemas.user import UserUpdate, UserResponse
from src.services.password import PasswordHandler
from src.services.upload_image import UploadImageService


class UserController:
    def __init__(
            self,
            uow: UoW,
            user_repository: UserRepository,
            profile_repository: ProfileRepository,
            image_service: UploadImageService,
            password_service: PasswordHandler
    ):
        self.uow = uow
        self.user_repository = user_repository
        self.profile_repository = profile_repository
        self.password_service = password_service
        self.image_service = image_service

    async def profile_user(self, user_id: int):
        db_user = await self.user_repository.get_user_by_id(user_id)
        if not db_user:
            raise BadRequestException("User with this id does not exist")
        return await self._get_me(user_id)

    async def profile_change(self, user_id: int, form: UserUpdate):
        db_user = await self.user_repository.get_user_by_id(user_id)
        if not db_user:
            raise BadRequestException("User not found")

        if form.username and form.username != db_user.username:
            if await self.user_repository.get_user_by_username(form.username):
                raise BadRequestException("Username already exists")

        if form.email and form.email != db_user.email:
            if await self.user_repository.get_user_by_email(form.email):
                raise BadRequestException("Email already exists")

        user_update = form.dict(
            exclude_unset=True, exclude={
                "password", "new_password", "verify_new_password",
                "first_name", "last_name", "gender", "language",
                "country", "date_of_birth", "profile_picture"
            }
        )
        profile_update = form.dict(
            exclude_unset=True,
            exclude={
                "email",
                "username",
                "password",
                "new_password",
                "verify_new_password"
            }
        )

        if form.password:
            if not form.new_password or not form.verify_new_password:
                raise BadRequestException("New password fields required")
            if not self.password_service.verify(db_user.password, form.password):
                raise BadRequestException("Incorrect current password")
            if form.new_password != form.verify_new_password:
                raise BadRequestException("Passwords do not match")

            user_update["password"] = self.password_service.hash(form.new_password)

        async with self.uow:
            if user_update:
                await self.user_repository.update_user(user_id, user_update)

            db_profile = await self.profile_repository.get_profile_by_user_id(user_id)
            if not db_profile:
                await self.profile_repository.create_profile({"user_id": user_id})

            if profile_update:
                if form.profile_picture is not None:
                    new_name = await self.image_service.upload_image(form.profile_picture)
                    if db_profile.profile_picture:
                        await self.image_service.delete_image(db_profile.profile_picture)
                    profile_update["profile_picture"] = new_name
                await self.profile_repository.update_profile(user_id, profile_update)

        return await self._get_me(user_id)

    async def _get_me(self, user_id: int) -> UserResponse:
        db_user = await self.user_repository.get_user_by_id(user_id)
        if not db_user:
            raise NotFoundException("User not found")

        user_dict = {
            "id": db_user.id,
            "email": db_user.email,
            "username": db_user.username,
            "role": db_user.role,
        }

        if db_user.profile:
            user_dict['profile'] = {
                'id': db_user.profile.id,
                "first_name": db_user.profile.first_name,
                "last_name": db_user.profile.last_name,
                "gender": db_user.profile.gender,
                "language": db_user.profile.language,
                "country": db_user.profile.country,
                "date_of_birth": db_user.profile.date_of_birth,
                "profile_picture": f"media/{db_user.profile.profile_picture}",
            }

        return UserResponse(**user_dict)
