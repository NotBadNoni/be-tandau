# src/di/controllers_di.py

from dishka import Provider, Scope, provide

from src.controllers.auth import AuthController
from src.controllers.chat import ChatController
from src.controllers.speciality import SpecialtyController
from src.controllers.subject import SubjectController
from src.controllers.subject_combination import SubjectCombinationController
from src.controllers.subject_combination_specialties import SubjectCombinationSpecialtiesController
from src.controllers.university import UniversityController
from src.controllers.university_specialties import UniversitySpecialtiesController
from src.controllers.user import UserController
from src.core.databases import UoW
from src.repositories.chat import ChatRepository, ChatMessageRepository
from src.repositories.profile import ProfileRepository
from src.repositories.speciality import SpecialtyRepository
from src.repositories.subject import SubjectRepository
from src.repositories.subject_combination import SubjectCombinationRepository
from src.repositories.subject_combination_specialties import SubjectCombinationSpecialtiesRepository
from src.repositories.university import UniversityRepository
from src.repositories.university_specialties import UniversitySpecialtiesRepository
from src.repositories.user import UserRepository
from src.services.email_service import EmailService
from src.services.openai_cli import OpenAIClient
from src.services.password import PasswordHandler
from src.services.redis_service import RedisService
from src.services.security import JWTHandler
from src.services.upload_image import UploadImageService


class ControllersDi(Provider):
    scope = Scope.REQUEST

    @provide
    def get_auth_container(
            self,
            uow: UoW,
            user_repository: UserRepository,
            profile_repository: ProfileRepository,
            password_handler: PasswordHandler,
            jwt_handler: JWTHandler,
            email_service: EmailService,
            redis_service: RedisService,
    ) -> AuthController:
        return AuthController(
            uow,
            user_repository,
            profile_repository,
            password_handler,
            jwt_handler,
            email_service,
            redis_service
        )

    @provide
    def get_user_container(
            self,
            uow: UoW,
            user_repository: UserRepository,
            profile_repository: ProfileRepository,
            image_service: UploadImageService,
            password_handler: PasswordHandler
    ) -> UserController:
        return UserController(uow, user_repository, profile_repository, image_service, password_handler)

    @provide
    def get_universal_container(
            self,
            uow: UoW,
            university_repository: UniversityRepository,
    ) -> UniversityController:
        return UniversityController(uow, university_repository)

    @provide
    def get_subject_container(
            self,
            uow: UoW,
            subject_repository: SubjectRepository
    ) -> SubjectController:
        return SubjectController(uow, subject_repository)

    @provide
    def get_specialty_container(
            self,
            uow: UoW,
            specialty_repository: SpecialtyRepository
    ) -> SpecialtyController:
        return SpecialtyController(uow, specialty_repository)

    @provide
    def get_subject_combination_container(
            self,
            uow: UoW,
            subject_combination_repository: SubjectCombinationRepository
    ) -> SubjectCombinationController:
        return SubjectCombinationController(uow, subject_combination_repository)

    @provide
    def get_specialty_container(
            self,
            uow: UoW,
            specialty_repository: SpecialtyRepository,
            subject_combination_repository: SubjectCombinationRepository,
    ) -> SpecialtyController:
        return SpecialtyController(uow, specialty_repository, subject_combination_repository)

    @provide
    def get_subject_combination_specialties_container(
            self,
            uow: UoW,
            subject_combination_specialties_repository: SubjectCombinationSpecialtiesRepository,
            subject_combination_repository: SubjectCombinationRepository,
            specialty_repository: SpecialtyRepository
    ) -> SubjectCombinationSpecialtiesController:
        return SubjectCombinationSpecialtiesController(
            uow,
            subject_combination_specialties_repository,
            subject_combination_repository,
            specialty_repository
        )

    @provide
    def get_university_specialties_container(
            self,
            uow: UoW,
            university_specialties_repository: UniversitySpecialtiesRepository,
            university_repository: UniversityRepository,
            specialty_repository: SpecialtyRepository,
    ) -> UniversitySpecialtiesController:
        return UniversitySpecialtiesController(
            uow,
            university_specialties_repository,
            university_repository,
            specialty_repository
        )

    @provide
    def get_chat_controller(
            self,
            uow: UoW,
            chat_repository: ChatRepository,
            chat_message_repository: ChatMessageRepository,
            university_repository: UniversityRepository,
            openai_client: OpenAIClient,
    ) -> ChatController:
        return ChatController(
            uow,
            chat_repository,
            chat_message_repository,
            openai_client,
            university_repository
        )
