import redis.asyncio as aioredis
from fastapi import FastAPI
from core.setting.settings import settings
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

class RedisClient:
    _instance: Optional[aioredis.Redis] = None
    _lock = asyncio.Lock()  # 동시성 제어를 위한 락 추가

    @classmethod
    async def get_instance(cls) -> aioredis.Redis:
        async with cls._lock:
            if cls._instance is None:
                try:
                    logger.info("Redis 연결 초기화 중...")
                    cls._instance = await aioredis.from_url(
                        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                        db=settings.REDIS_DB,
                        password=settings.REDIS_PASSWORD,
                        encoding="utf-8",
                        decode_responses=True
                    )
                    await cls._instance.ping()
                    logger.info("Redis 연결 성공")
                except Exception as e:
                    logger.error(f"Redis 연결 실패: {str(e)}")
                    cls._instance = None  # 실패 시 None으로 설정
                    raise

            return cls._instance

    @classmethod
    async def close(cls) -> None:
        async with cls._lock:
            if cls._instance:
                try:
                    logger.info("Redis 연결 종료 중...")
                    await cls._instance.close()
                    cls._instance = None
                    logger.info("Redis 연결 종료 완료")
                except Exception as e:
                    logger.error(f"Redis 연결 종료 중 오류 발생: {str(e)}")
                    raise


def setup_redis(app: FastAPI) -> None:
    @app.on_event("startup")
    async def startup_redis_client() -> None:
        app.state.redis = await RedisClient.get_instance()
        logger.info("Redis client initialized and stored in app state")

    @app.on_event("shutdown")
    async def shutdown_redis_client() -> None:
        try:
            if hasattr(app.state, "redis") and app.state.redis is not None:
                await RedisClient.close()
                logger.info("Redis client shutdown completed")
        except Exception as e:
            logger.warning(f"Error during Redis shutdown: {e}")


# Redis 유틸리티 함수들
async def get_redis() -> aioredis.Redis:
    """Redis 인스턴스를 가져오는 유틸리티 함수"""
    instance = await RedisClient.get_instance()
    if not instance:
        raise RuntimeError("Redis client is not initialized")
    return instance

async def redis_set_with_ttl(key: str, value: str, ttl: int = 3600) -> None:
    """Redis에 데이터를 TTL과 함께 저장"""
    redis = await get_redis()
    await redis.set(key, value, ex=ttl)

async def redis_get(key: str) -> Optional[str]:
    """Redis에서 데이터 조회"""
    redis = await get_redis()
    return await redis.get(key)