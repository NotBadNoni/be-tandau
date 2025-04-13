from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.chat import ChatRepository, ChatMessageRepository
from src.repositories.profile import ProfileRepository
from src.repositories.speciality import SpecialtyRepository
from src.repositories.subject import SubjectRepository
from src.repositories.subject_combination import SubjectCombinationRepository
from src.repositories.subject_combination_specialties import SubjectCombinationSpecialtiesRepository
from src.repositories.university import UniversityRepository
from src.repositories.university_specialties import UniversitySpecialtiesRepository
from src.repositories.user import UserRepository


class RepositoriesDi(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_repo(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide
    def get_university_repo(self, session: AsyncSession) -> UniversityRepository:
        return UniversityRepository(session)

    @provide
    def get_subject_combination_repository(self, session: AsyncSession) -> SubjectCombinationRepository:
        return SubjectCombinationRepository(session)

    @provide
    def get_specialty_repository(self, session: AsyncSession) -> SpecialtyRepository:
        return SpecialtyRepository(session)

    @provide
    def get_subject_repository(self, session: AsyncSession) -> SubjectRepository:
        return SubjectRepository(session)

    @provide
    def get_profile_repository(self, session: AsyncSession) -> ProfileRepository:
        return ProfileRepository(session)

    @provide
    def get_subject_combination_specialties_repository(
            self,
            session: AsyncSession
    ) -> SubjectCombinationSpecialtiesRepository:
        return SubjectCombinationSpecialtiesRepository(session)

    @provide
    def get_university_specialties_repository(
            self,
            session: AsyncSession
    ) -> UniversitySpecialtiesRepository:
        return UniversitySpecialtiesRepository(session)

    @provide
    def get_chat_repository(self, session: AsyncSession) -> ChatRepository:
        return ChatRepository(session)

    @provide
    def get_chat_message_repository(self, session: AsyncSession) -> ChatMessageRepository:
        return ChatMessageRepository(session)
