from pydantic import BaseModel


class SourceBase(BaseModel):
    name: str
    url: str
    type: int
    is_active: bool
    role_id: int


class Source(SourceBase):
    id: int

    class Config:
        orm_mode = True
