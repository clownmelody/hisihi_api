import time

__author__ = 'shaolei'

from sqlalchemy import Column, Integer, SmallInteger, String
from herovii.models.base import Base


class UserRebateGift(Base):
    __tablename__ = 'hisihi_user_rebate_gift'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, unique=True)
    user_rebate_id = Column(Integer)
    name = Column(String)
    phone_num = Column(String)
    address = Column(String)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger, default=1)
    voucher = Column(String)
    check = Column(SmallInteger, default=0)

    def keys(self):
        return (
            'id', 'uid', 'user_rebate_id', 'name', 'phone_num', 'address', 'voucher', 'check'
        )