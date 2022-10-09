from typing import List

from fastapi import APIRouter

from anaserver import crud, models, schemas
from anaserver.database import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.User)
async def read_users() -> List[schemas.User]:
    db = get_session()
    users_orm = await crud.get_users(db)
    users = [schemas.User(id=user.id, role_id=user.role) for user in users_orm]
    return users


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate) -> schemas.User:
    db = get_session()
    user_orm = models.User(id=user.id, role_id=user.role_id)
    result_orm = await crud.add_user(db, user_orm)
    result = schemas.User(id=result_orm.id, role_id=result_orm.role)
    return result
