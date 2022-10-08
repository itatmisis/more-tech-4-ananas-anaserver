from pydantic import BaseModel


class NewsEmbeddingBase(BaseModel):
    embedding: list
    cluster_id: int


class NewsEmbedding(NewsEmbeddingBase):
    news_id: int

    class Config:
        orm_mode = True
