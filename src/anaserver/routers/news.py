from typing import List
from uuid import UUID

from fastapi import APIRouter

from anaserver import crud, schemas
from anaserver.database import get_session

router = APIRouter(
    prefix="/news",
    tags=["news"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.News])
async def read_news() -> List[schemas.News]:
    async with get_session() as db:
        news_orm = await crud.get_all_news(db)
        news = [schemas.News.from_orm(news) for news in news_orm]
        return news


@router.get("/{news_id}", response_model=schemas.News)
async def read_news_by_id(news_id: UUID) -> schemas.News:
    async with get_session() as db:
        news_orm = await crud.get_news_by_id(db, news_id)
        news = schemas.News.from_orm(news_orm)
        return news


@router.get("/user/{user_id}", response_model=List[schemas.News])
async def get_news_for_user(user_id: int) -> List[schemas.News]:
    async with get_session() as db:
        news_orm = await crud.get_news_for_user(db, user_id, 3)
        news = [schemas.News.from_orm(news) for news in news_orm]
        return news


@router.get("/trends/{role_id}", response_model=List[schemas.News])
async def get_trends_for_role(role_id: int) -> List[schemas.News]:
     async with get_session() as db:
        news_orm = await crud.get_trends_for_role(db, role_id)
        news = [schemas.News.from_orm(news) for news in news_orm]
        return news
