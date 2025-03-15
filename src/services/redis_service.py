from src.core.redis import RedisEngine


class RedisService:
    def __init__(self, redis_engine: RedisEngine):
        self.redis_client = redis_engine.redis

    async def get(self, key):
        return await self.redis_client.get(key)

    async def set(self, key, value, expire=None):
        await self.redis_client.set(key, value)
        if expire:
            await self.redis_client.expire(key, expire)

    async def delete(self, key):
        await self.redis_client.delete(key)
