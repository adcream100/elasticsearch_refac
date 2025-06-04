from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Response, Query, Cookie
from typing import List, Optional, Tuple

from app.di.container import Container
from app.keywords.application.services.keyword_service import KeywordService

from app.keywords.application.dto.keyword_dto import (
    PopularSearchResponseDto,
    UpdatePopularRequestDto
)

router = APIRouter(prefix="/keywords")

@router.get("/get_popular_searches", summary="인기 검색어 조회")
@inject
async def get_popular_searches(
    category: str = Query(None),
    limit: int = Query(10, ge=1, le=100),
    keyword_service: KeywordService = Depends(Provide[Container.keyword_service]),
) -> List[PopularSearchResponseDto]:
    return await keyword_service.get_popular_searches(category, limit)

@router.post("/update_popular_search", summary="인기 검색어 업데이트")
@inject
async def update_popular_search(
    update_data: UpdatePopularRequestDto,
    keyword_service: KeywordService = Depends(Provide[Container.keyword_service]),
):
    return await keyword_service.update_popular_search(update_data=update_data)

@router.post("/add_recent_search", summary="인기 검색어 업데이트")
@inject
async def update_popular_search_before(
    request: Request,
    response: Response,
    update_data: UpdatePopularRequestDto,
    auth_result: Tuple[Optional[UserResponse], AuthStatus, Request] = Depends(
        get_optional_user
    ),
    anonymous_id: Optional[str] = Cookie(None),
    keyword_service: KeywordService = Depends(Provide[Container.keyword_service]),
):
    return await keyword_service.add_recent_search()