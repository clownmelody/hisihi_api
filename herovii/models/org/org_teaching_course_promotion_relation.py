from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer
from herovii.models.base import Base


class OrgTeachingCoursePromotionRelation(Base):
    __tablename__ = 'hisihi_teaching_course_organization_promotion_relation'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    teaching_course_id = Column(Integer, nullable=False)
    organization_id = Column(Integer, nullable=False)
    promotion_id = Column(Integer, nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)
