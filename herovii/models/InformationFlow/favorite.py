from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base, db

__author__ = 'yangchujie'


class Favorite(db.Model):

    __tablename__ = 'hisihi_favorite'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    appname = Column(String(45), nullable=False)
    row = Column(Integer, nullable=True)
    uid = Column(Integer, nullable=True)
