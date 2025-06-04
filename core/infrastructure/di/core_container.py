# -*- coding: utf-8 -*-
from dependency_injector import containers, providers

from core.infrastructure.database.database import Database

from core.infrastructure.redis.client import RedisClient

async def provide_redis_client():
    return await RedisClient.get_instance()


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)

    database = providers.Singleton(
        Database,
        database_user=config.mssql_user,
        database_password=config.mssql_pass,
        database_host=config.mssql_host,
        database_port=config.mssql_port,
        database_name=config.mssql_db,
    )

    redis_client = providers.Resource(provide_redis_client)