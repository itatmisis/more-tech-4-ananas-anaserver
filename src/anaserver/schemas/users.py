from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    id: int
    role: int


class User(UserBase):
    id: int
    role: int

    class Config:
        orm_mode = True
