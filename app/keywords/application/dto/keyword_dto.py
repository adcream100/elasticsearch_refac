from core.applications.dtos.dto import BaseRequest, BaseResponse

class PopularSearchResponseDto(BaseResponse):
    term: str
    category: str
    count: int

class UpdatePopularRequestDto(BaseRequest):
    term: str
    category: str