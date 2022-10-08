import sqlalchemy

from anaserver.database import Base


class Action(Base):
    __tablename__ = "actions"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
