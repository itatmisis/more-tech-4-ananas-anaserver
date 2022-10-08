from pydantic import BaseModel


class ActionBase(BaseModel):
    name: str


class Action(ActionBase):
    id: int

    class Config:
        orm_mode = True
