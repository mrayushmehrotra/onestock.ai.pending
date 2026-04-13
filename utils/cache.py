import redis.asyncio as redis
from config.settings import settings
from utils.logger import logger
import json

class CacheManager:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def set(self, key: str, value: any, expire: int = 3600):
        try:
            await self.redis.set(key, json.dumps(value), ex=expire)
        except Exception as e:
            logger.error(f"Cache SET failed: {e}")

    async def get(self, key: str):
        try:
            val = await self.redis.get(key)
            return json.loads(val) if val else None
        except Exception as e:
            logger.error(f"Cache GET failed: {e}")
            return None

cache = CacheManager()
