from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base, db

__author__ = 'yangchujie'


class Picture(db.Model):

    __tablename__ = 'hisihi_picture'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    path = Column(String(255), nullable=False)
