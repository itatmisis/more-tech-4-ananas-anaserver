from typing import List

from pydantic import BaseModel


class UserEmbeddingBase(BaseModel):
    embedding: List[float]


class UserEmbedding(UserEmbeddingBase):
    id: int

    class Config:
        orm_mode = True
