from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def create_dsn(
    database_user: str,
    database_password: str,
    database_host: str,
    database_port: int,
    database_name: str,
):
    return f"mssql+pyodbc://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(
        self,
        database_user: str,
        database_password: str,
        database_host: str,
        database_port: int,
        database_name: str,
    ) -> None:
        dsn = create_dsn(
            database_user=database_user,
            database_password=database_password,
            database_host=database_host,
            database_port=database_port,
            database_name=database_name,
        )

        self.engine = create_async_engine(url=dsn, echo=True)

        self.async_session_factory = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self):
        async with self.async_session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
