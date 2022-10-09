import sqlalchemy

from anaserver.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    url = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.Integer)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean)
    role_id = sqlalchemy.Column(sqlalchemy.ForeignKey("roles.id"))
