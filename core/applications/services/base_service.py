import logging
from abc import ABC, abstractmethod
from typing import List, Type, TypeVar, Generic, Optional

from core.applications.dtos.dto import BaseRequest, BaseResponse
from core.infrastructure.repositories.base_repository import BaseRepository

CreateDTO = TypeVar("CreateDTO", bound=BaseRequest)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseRequest)
ResponseDTO = TypeVar("ResponseDTO", bound=BaseResponse)

class BaseService(ABC, Generic[CreateDTO, ResponseDTO, UpdateDTO]):

    def __init__(self, repository: BaseRepository):
        self.repository = repository
        self.logger = logging.getLogger(self.__class__.__name__)

    async def create(self, data: CreateDTO) -> ResponseDTO:
        result = await self.repository.create_data(create_data=data)
        return self._to_response_dto(result)

    async def bulk_create(self, datas: List[CreateDTO]) -> List[ResponseDTO]:
        results = await self.repository.create_datas(create_datas=datas)
        return [self._to_response_dto(r) for r in results]

    async def list(self, page: int, page_size: int) -> List[ResponseDTO]:
        results = await self.repository.get_datas(page=page, page_size=page_size)
        return [self._to_response_dto(r) for r in results]

    async def get(self, data_id: int) -> Optional[ResponseDTO]:
        result = await self.repository.get_data_by_data_id(data_id=data_id)
        return self._to_response_dto(result) if result else None

    async def update(self, data_id: int, data: UpdateDTO) -> Optional[ResponseDTO]:
        result = await self.repository.update_data_by_data_id(
            data_id=data_id, update_data=data
        )
        return self._to_response_dto(result) if result else None

    async def delete(self, data_id: int) -> None:
        await self.repository.delete_data_by_data_id(data_id=data_id)

    @abstractmethod
    def _to_response_dto(self, entity) -> ResponseDTO:
        return entity
