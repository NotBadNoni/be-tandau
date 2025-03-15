from redis.asyncio import Redis

from src.core.config import settings


class RedisEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisEngine, cls).__new__(cls)
            cls._instance.redis = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
            )
        return cls._instance

    async def close(self):
        if self.redis:
            await self.redis.close()
            self.redis = None
