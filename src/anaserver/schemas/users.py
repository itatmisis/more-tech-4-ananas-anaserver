from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    id: int
    role_id: int


class User(UserBase):
    id: int
    role_id: int

    class Config:
        orm_mode = True
