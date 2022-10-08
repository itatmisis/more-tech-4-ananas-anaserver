from pydantic import BaseModel


class NewsBase(BaseModel):
    text: str
    short_text: str
    url: str
    views: int
    date: str


class News(NewsBase):
    id: int
    source_id: int

    class Config:
        orm_mode = True
