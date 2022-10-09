import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from anaserver.database import Base


class UserToNews(Base):
    __tablename__ = "users_to_news"

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    news_id = sqlalchemy.Column(UUID(as_uuid=True), sqlalchemy.ForeignKey("news.id"))
    action_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("actions.id"))
    compound_key = sqlalchemy.PrimaryKeyConstraint(user_id, news_id, action_id)
