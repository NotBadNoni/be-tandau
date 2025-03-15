from dishka import Scope, provide, Provider

from src.core.redis import RedisEngine
from src.services.email_service import EmailService
from src.services.password import PasswordHandler
from src.services.redis_service import RedisService
from src.services.security import JWTHandler


class ServicesDi(Provider):
    scope = Scope.APP

    @provide
    def get_email_service(self) -> EmailService:
        return EmailService()

    @provide
    def get_redis_service(self, redis_engine: RedisEngine) -> RedisService:
        return RedisService(redis_engine)

    @provide
    def get_hash_service(self) -> PasswordHandler:
        return PasswordHandler()

    @provide
    def get_jwt_service(self) -> JWTHandler:
        return JWTHandler()