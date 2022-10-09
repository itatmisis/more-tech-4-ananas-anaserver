from pgvector.sqlalchemy import Vector
import sqlalchemy

from anaserver.database import Base


class UserEmbedding(Base):
    __tablename__ = "users_embeddings"

    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True)
    embedding = sqlalchemy.Column(Vector(256))
