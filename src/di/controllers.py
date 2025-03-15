from dishka import Provider, Scope, provide

from src.controllers.auth import AuthController
from src.controllers.user import UserController
from src.core.databases import UoW
from src.repositories.user import UserRepository
from src.services.email_service import EmailService
from src.services.password import PasswordHandler
from src.services.redis_service import RedisService
from src.services.security import JWTHandler


class ControllersDi(Provider):
    scope = Scope.REQUEST

    @provide
    def get_auth_container(
            self,
            uow: UoW,
            user_repository: UserRepository,
            password_handler: PasswordHandler,
            jwt_handler: JWTHandler,
            email_service: EmailService,
            redis_service: RedisService,
    ) -> AuthController:
        return AuthController(
            uow,
            user_repository,
            password_handler,
            jwt_handler,
            email_service,
            redis_service
        )

    @provide
    def get_user_container(self, uow: UoW, user_repository: UserRepository) -> UserController:
        return UserController(uow, user_repository)
