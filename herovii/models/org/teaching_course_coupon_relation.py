from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class TeachingCourseCouponRelation(Base):
    __tablename__ = 'hisihi_teaching_course_coupon_relation'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    teaching_course_id = Column(Integer, nullable=False)
    coupon_id = Column(Integer, nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)
    service_condition = Column(String(200), nullable=False)
    using_method = Column(String(200), nullable=False)
    instructions_for_use = Column(String(200), nullable=False)
    gift_package_id = Column(Integer)
