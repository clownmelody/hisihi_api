import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, SmallInteger
from herovii.models.base import Base


class UserCoupon(Base):
    __tablename__ = 'hisihi_user_coupon'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, unique=True)
    coupon_id = Column(Integer, unique=True)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger, default=1)

    def keys(self):
        return (
            'id', 'uid', 'coupon_id'
        )