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
    db = get_session()
    users_orm = await crud.get_users(db)
    users = [schemas.User(id=user.id, role=user.role) for user in users_orm]
    return users


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate) -> schemas.User:
    db = get_session()
    user_orm = models.User(id=user.id, role=user.role)
    result_orm = await crud.add_user(db, user_orm)
    result = schemas.User(id=result_orm.id, role=result_orm.role)
    return result


@router.get("/user_embeddings", response_model=list)
async def user_embeddings(user_id: int) -> list:
    db = get_session()
    return await crud.get_user_embedding(db, user_id)
