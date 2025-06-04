from core.infrastructure.redis.client import RedisClient

from itertools import islice

from app.keywords.infrastructure.entities.entity import (
    PopularSearchEntity
)

class KeywordRedisRepository:
    def __init__(self, client: RedisClient):
        self.client = client

    async def get_popular_searches(self, category=None, limit=10):
        searches = await self.client.zrevrange("popular_searches", 0, -1, withscores=True)
        
        return [
            PopularSearchEntity(term=term, category=cat, count=int(count))
            for search, count in searches
            if (term := search.split(":")[0]) and (cat := search.split(":")[1])
            and (not category or cat == category)
        ][:limit]

    async def inc_popular_search(self, term, category):
        await self.client.zincrby("popular_searches", 1, f"{term}:{category}")

    async def add_recent_search(self, redis_key, term, category):
        await self.client.lpush(redis_key, f"{term}:{category}")
        await self.client.ltrim(redis_key, 0, 19)  # 최대 20개 유지

    async def get_recent_searches(self, redis_key, category=None):
        searches = await self.client.lrange(redis_key, 0, -1)
        result, seen = [], set()
        for search in searches:
            t, c = search.split(":")
            if not category or c == category:
                item = (t, c)
                if item not in seen:
                    seen.add(item)
                    result.append({"term": t, "category": c})
            if len(result) == 20:
                break
        return result
