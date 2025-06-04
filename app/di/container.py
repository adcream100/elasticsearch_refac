from core.infrastructure.di.core_container import CoreContainer
from dependency_injector import providers

from app.keywords.infrastructure.repositories.keyword_repository import KeywordRepository
from app.keywords.infrastructure.repositories.redis_repository import KeywordRedisRepository

from app.keywords.application.services.keyword_service import KeywordService

class Container(CoreContainer):
    keyword_repository = providers.Singleton(
        KeywordRepository,
        session=CoreContainer.database.provided.session
    )

    keyword_redis_repository = providers.Singleton(
        KeywordRedisRepository,
        client=CoreContainer.redis_client
    )

    # ------------------------------------------

    keyword_service = providers.Factory(
        KeywordService,
        keyword_repository=keyword_repository,
        keyword_redis_repository=keyword_redis_repository
    )