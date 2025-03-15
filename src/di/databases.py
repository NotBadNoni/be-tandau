from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from src.core.config import settings
from src.core.databases import create_engine, create_session, UoW
from src.core.redis import RedisEngine


class DatabasesDi(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        """Создаём движок SQLAlchemy."""
        engine = await create_engine(settings.async_db_url)
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        """Создаём фабрику сессий."""
        return await create_session(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_uow(self, session: AsyncSession) -> UoW:
        return UoW(session)

    @provide(scope=Scope.APP)
    def get_redis_engine(self) -> RedisEngine:
        return RedisEngine()