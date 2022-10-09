from typing import List

from fastapi import APIRouter, status

from anaserver import crud, schemas
from anaserver.database import get_session

router = APIRouter(
    prefix="/actions",
    tags=["actions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=List[schemas.News])
async def add_action(action: schemas.ActionCreate):
    with get_session() as db:
        try:
            await crud.add_action(db, user_id=action.user_id, news_id=action.news_id, action_id=action.id)
            return status.HTTP_200_OK
        except Exception:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
