from pydantic import BaseModel
from datetime import datetime


class NewsBase(BaseModel):
    text: str
    short_text: str
    url: str
    views: int
    date: datetime


class News(NewsBase):
    id: int
    source_id: int

    class Config:
        orm_mode = True
