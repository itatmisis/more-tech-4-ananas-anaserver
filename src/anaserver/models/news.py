import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from anaserver.database import Base


class News(Base):
    __tablename__ = "news"

    id = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, index=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    short_text = sqlalchemy.Column(sqlalchemy.String)
    url = sqlalchemy.Column(sqlalchemy.String)
    views = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    source_id = sqlalchemy.Column(sqlalchemy.ForeignKey("sources.id"))

    attachments = relationship("Attachment", backref="news")
