from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import SmallInteger
from herovii.models.base import Base
import time
__author__ = 'shaolei'


class RebateOrder(Base):
    __tablename__ = 'hisihi_order'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    order_sn = Column(String(30), nullable=False)
    uid = Column(Integer, nullable=False)
    mobile = Column(String(60), nullable=False)
    order_status = Column(SmallInteger, default=0)
    price = Column(Integer, default=0)
    pay_type = Column(SmallInteger)
    pay_status = Column(SmallInteger, default=0)
    courses_id = Column(Integer, nullable=False)
    organization_id = Column(Integer, nullable=False)
    rebate_id = Column(Integer, nullable=False)
    rebate_num = Column(Integer, default=1)
    create_time = Column(Integer, default=int(time.time()))
    pay_time = Column(Integer)
    status = Column(SmallInteger, default=0)

    def __init__(self, **entries):
        self.__dict__.update(entries)
        super(RebateOrder, self).__init__()

    def keys(self):
        return (
            'id', 'order_sn', 'uid', 'mobile', 'order_status', 'pay_type', 'pay_status', 'courses_id',
            'organization_id', 'rebate_id', 'rebate_num', 'create_time', 'pay_time', 'status', 'price'
        )

