from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Callable, Generic, List, Type, TypeVar, Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.entities.entity import Entity
from core.infrastructure.database.database import Base

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]

CreateEntity = TypeVar("CreateEntity", bound=Entity)
ReturnEntity = TypeVar("ReturnEntity", bound=Entity)
UpdateEntity = TypeVar("UpdateEntity", bound=Entity)

class BaseRepository(ABC, Generic[CreateEntity, ReturnEntity, UpdateEntity]):
    def __init__(self, session_factory: SessionFactory) -> None:
        self.session_factory = session_factory

    @property
    @abstractmethod
    def model(self) -> Type[Base]:
        raise NotImplementedError

    @property
    @abstractmethod
    def entity_cls(self) -> Type[ReturnEntity]:
        raise NotImplementedError

    def _to_entity(self, orm_obj) -> ReturnEntity:
        return self.entity_cls(**vars(orm_obj))

    async def create_data(self, create_data: CreateEntity) -> ReturnEntity:
        async with self.session_factory() as session:
            orm_obj = self.model(**create_data.model_dump(exclude_none=True))
            session.add(orm_obj)
            await session.commit()
            await session.refresh(orm_obj)
        return self._to_entity(orm_obj)

    async def create_datas(self, create_datas: List[CreateEntity]) -> List[ReturnEntity]:
        async with self.session_factory() as session:
            values = [cd.model_dump(exclude_none=True) for cd in create_datas]
            result = await session.execute(insert(self.model).values(values))
            await session.commit()
            
            ids = [row[0] for row in result.inserted_primary_key_rows]
            result = await session.execute(select(self.model).where(self.model.id.in_(ids)))
            return [self._to_entity(obj) for obj in result.scalars().all()]

    async def get_datas(self, page: int, page_size: int) -> List[ReturnEntity]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model).offset((page - 1) * page_size).limit(page_size)
            )
            return [self._to_entity(obj) for obj in result.scalars().all()]

    async def get_data_by_data_id(self, data_id: int) -> Optional[ReturnEntity]:
        async with self.session_factory() as session:
            result = await session.execute(select(self.model).filter(self.model.id == data_id))
            obj = result.scalar_one_or_none()
        return self._to_entity(obj) if obj else None

    async def get_datas_by_data_id(self, data_id: int, page: int, page_size: int) -> List[ReturnEntity]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model)
                .filter(self.model.id == data_id)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            return [self._to_entity(obj) for obj in result.scalars().all()]

    async def update_data_by_data_id(self, data_id: int, update_data: UpdateEntity) -> Optional[ReturnEntity]:
        async with self.session_factory() as session:
            result = await session.execute(select(self.model).filter(self.model.id == data_id))
            obj = result.scalar_one_or_none()
            if not obj:
                return None
            for key, value in update_data.model_dump(exclude_none=True).items():
                setattr(obj, key, value)
            await session.commit()
            await session.refresh(obj)
        return self._to_entity(obj)

    async def delete_data_by_data_id(self, data_id: int) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(select(self.model).filter(self.model.id == data_id))
            obj = result.scalar_one_or_none()
            if not obj:
                return False
            await session.delete(obj)
            await session.commit()
            return True
