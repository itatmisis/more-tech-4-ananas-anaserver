from pydantic import BaseModel


class SourceBase(BaseModel):
    name: str
    url: str
    type: int


class Source(SourceBase):
    id: int

    class Config:
        orm_mode = True
