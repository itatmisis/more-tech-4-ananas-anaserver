import sqlalchemy

from anaserver.database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    type = sqlalchemy.Column(sqlalchemy.Integer)
    url = sqlalchemy.Column(sqlalchemy.String)
    news_id = sqlalchemy.Column(sqlalchemy.ForeignKey("news.id"))
