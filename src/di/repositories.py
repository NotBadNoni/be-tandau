from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.university import UniversityRepository
from src.repositories.user import UserRepository


class RepositoriesDi(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_repo(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide
    def get_university_repo(self, session: AsyncSession) -> UniversityRepository:
        return UniversityRepository(session)
