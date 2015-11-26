__author__ = 'bliss'

import datetime
from sqlalchemy import Column, Integer, String, SmallInteger, Boolean
from herovii.models.base import Base


class OrderDuiBa(Base):

    __tablename__ = 'hisihi_order_duiba'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    credits = Column('credits', Integer)
    appKey = Column(String(255), nullable=False)

    # 兑吧的扣分申请时间
    deduct_timestamp = Column(Integer)

    # 兑吧兑换结果反馈时间
    confirm_timestamp = Column(Integer)

    description = Column(String(255))

    # 自有订单号
    bizId = Column(String(255))

    # 由兑吧生成的订单号
    orderNum = Column(String(255), nullable=False)
    type = Column(String(255))
    facePrice = Column('facePrice', Integer)
    actualPrice = Column('actualPrice', Integer)
    ip = Column(String(60))
    waitAudit = Column('waitAudit', Boolean)
    params = Column(String(255))
    sign = Column(String(255))

    # 订单是否兑换成功，0：等待兑吧反馈， 1：兑换成功， -1：兑换失败
    success = Column(SmallInteger, default=0)
    error_message = Column(String(255))
    # status = Column(SmallInteger, default=1)

    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.deduct_timestamp = entries['timestamp']
        super(OrderDuiBa, self).__init__()



