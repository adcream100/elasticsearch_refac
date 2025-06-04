from app.keywords.infrastructure.repositories.keyword_repository import KeywordRepository
from app.keywords.infrastructure.repositories.redis_repository import KeywordRedisRepository

from app.keywords.application.dto.keyword_dto import (
    UpdatePopularRequestDto
)

class KeywordService:
    def __init__(self, 
                 keyword_repository: KeywordRepository,
                 keyword_redis_repository: KeywordRedisRepository):
        self.rdb_repo = keyword_repository
        self.redis_repo = keyword_redis_repository

    async def get_popular_searches(self, category=None, limit=10):
        return await self.redis_repo.get_popular_searches(category, limit)

    async def update_popular_search(self, update_data: UpdatePopularRequestDto):
        await self.rdb_repo.update_popular_search(term=update_data.term, category=update_data.category)
        await self.redis_repo.inc_popular_search(term=update_data.term, category=update_data.category)
        return {"status": "success"}

    async def add_recent_search(self, db, redis_key, term, category, user_info=None):
        if user_info: 
            await self.rdb_repo.add_recent_search(db, user_info.UserId, term, category)
        else:  
            pass
        await self.redis_repo.add_recent_search(redis_key, term, category)
        return {"status": "success"}

    async def get_recent_searches(self, redis_key, db=None, user_id=None, category=None):
        # 우선 redis에서
        result = await self.redis_repo.get_recent_searches(redis_key, category)
        if len(result) < 20 and db and user_id:
            db_result = await self.rdb_repo.get_user_recent_searches(db, user_id, category, 20 - len(result))
            result += db_result
        return result[:20]
