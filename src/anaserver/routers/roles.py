from typing import List
from uuid import UUID

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
        return await crud.get_role_embedding(db, role_id);


