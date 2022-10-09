from pydantic import BaseModel


class SourceBase(BaseModel):
    name: str
    url: str
    type: int
    is_active: bool


class Source(SourceBase):
    id: int

    class Config:
        orm_mode = True
