from uuid import UUID

from pydantic import BaseModel


class ActionBase(BaseModel):
    pass


class ActionCreate(ActionBase):
    id: int
    user_id: int
    news_id: UUID


class Action(ActionBase):
    id: int
    name: str

    class Config:
        orm_mode = True
