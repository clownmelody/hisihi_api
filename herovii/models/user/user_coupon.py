import time


__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, SmallInteger, String
from herovii.models.base import Base


class UserCoupon(Base):
    __tablename__ = 'hisihi_user_coupon'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, unique=True, nullable=False)
    coupon_id = Column(Integer, unique=True, nullable=False)
    teaching_course_id = Column(Integer, nullable=False)
    promo_code = Column(String(30), nullable=False)
    promo_code_url = Column(String(100), nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger, default=1)

    def keys(self):
        return (
            'id', 'uid', 'coupon_id', 'teaching_course_id', 'promo_code', 'promo_code_url'
        )
