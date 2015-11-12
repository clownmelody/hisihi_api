__author__ = 'bliss'

import datetime
from sqlalchemy import Column, Integer, String, SmallInteger, Boolean
from herovii.models.base import Base


class OrderDuiBa(Base):

    __tablename__ = 'hisihi_order_duiba'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column('uid', Integer)
    credits = Column('credits', Integer)
    appKey = Column(String(255))
    timestamp = Column(String(20))
    description = Column(String(255))
    orderNum = Column(String(255))
    type = Column(String(255))
    facePrice = Column('facePrice', Integer)
    actualPrice = Column('actualPrice', Integer)
    ip = Column(String(60))
    waitAudit = Column('waitAudit', Boolean)
    params = Column(String(255))
    sign = Column(String(255))
    status = Column(SmallInteger, default=1)

    def __init__(self, **entries):
        self.__dict__.update(entries)



