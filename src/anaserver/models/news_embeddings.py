from pgvector.sqlalchemy import Vector
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from anaserver.database import Base


class NewsEmbedding(Base):
    __tablename__ = "news_embeddings"

    id = sqlalchemy.Column(UUID, sqlalchemy.ForeignKey("news.id"), primary_key=True)
    embedding = sqlalchemy.Column(Vector(256))
    cluster_id = sqlalchemy.Column(sqlalchemy.Integer)
