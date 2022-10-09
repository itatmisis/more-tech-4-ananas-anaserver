from typing import List

from fastapi import APIRouter

from anaserver import crud, schemas
from anaserver.database import get_session

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[float])
async def read_news(role_id: int) -> List[float]:
    async with get_session() as db:
        return await crud.get_role_embedding(db, role_id)


@router.get("/trend", response_model=schemas.News)
async def trend_for_role(role_id: int) -> schemas.News:
    db = get_session()
    news_orm = await crud.get_trends_for_role(db, role_id)
    return schemas.News.from_orm(news_orm)
