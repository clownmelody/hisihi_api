import time


__author__ = 'shaolei'

from sqlalchemy import Column, Integer, SmallInteger, String
from herovii.models.base import Base


class UserRebate(Base):
    __tablename__ = 'hisihi_user_rebate'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, unique=True, nullable=False)
    order_id = Column(Integer, unique=True, nullable=False)
    rebate_id = Column(Integer, unique=True, nullable=False)
    teaching_course_id = Column(Integer, nullable=False)
    promo_code = Column(String(30), nullable=False)
    promo_code_url = Column(String(100), nullable=False)
    bind_weixin_id = Column(Integer, default=0, nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger, default=0)

    def keys(self):
        return (
            'id', 'uid', 'order_id', 'coupon_id', 'teaching_course_id', 'promo_code', 'promo_code_url',
            'bind_weixin_id', 'status'
        )
