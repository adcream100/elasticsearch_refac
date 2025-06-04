from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import select, and_, func
from core.models.model import PopularSearches
from sqlalchemy.ext.asyncio import AsyncSession

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]

class KeywordRepository:
    def __init__(self, session: SessionFactory) -> None:
        self.session = session

    async def get_popular_searches(self, duration_days=30, limit=100):
        today = func.current_date()
        duration_ago = func.current_date() - duration_days
        async with self.session as session:
            query = (
                select(
                    PopularSearches.search_term,
                    PopularSearches.search_category,
                    func.sum(PopularSearches.search_count).label("total_count"),
                )
                .where(PopularSearches.search_date >= duration_ago)
                .group_by(PopularSearches.search_term, PopularSearches.search_category)
                .order_by(func.sum(PopularSearches.search_count).desc())
                .limit(limit)
            )
            result = await session.execute(query)
            return result.fetchall()

    async def update_popular_search(self, term, category, today):
        async with self.session as session:
            result = await session.execute(
                select(PopularSearches).where(
                    and_(
                        PopularSearches.search_term == term,
                        PopularSearches.search_category == category,
                        PopularSearches.search_date == today,
                    )
                )
            )

            existing_searches = result.fetchall()  # 모든 결과 가져오기

            if existing_searches:
                # 첫 번째 레코드만 업데이트하고 나머지는 삭제
                first_search = existing_searches[0][0]  # first()[0]로 실제 객체 가져오기
                first_search.search_count += 1

                # 중복된 레코드가 있다면 삭제
                if len(existing_searches) > 1:
                    for duplicate in existing_searches[1:]:
                        await session.delete(duplicate[0])
            else:
                # 새 레코드 추가
                new_search = PopularSearches(
                    search_term=term,
                    search_category=category,
                    search_date=today,
                    search_count=1,
                )
                session.add(new_search)
