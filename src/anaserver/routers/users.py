from typing import List

from fastapi import APIRouter

from anaserver import crud, models, schemas
from anaserver.database import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.User])
async def read_users() -> List[schemas.User]:
    with get_session() as db:
        users_orm = await crud.get_users(db)
        users = [schemas.User.from_orm(user) for user in users_orm]
        return users


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate) -> schemas.User:
    with get_session() as db:
        user_orm = models.User(id=user.id, role_id=user.role_id)
        result_orm = await crud.add_user(db, user_orm)
        result = schemas.User.from_orm(result_orm)
        return result
