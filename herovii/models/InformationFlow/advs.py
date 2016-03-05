from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base, db

__author__ = 'yangchujie'


class Advs(db.Model):

    __tablename__ = 'hisihi_advs'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    advspic_640_960 = Column(Integer, nullable=True)
    link = Column(String(140), nullable=True)
