from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class TeachingCourseOutline(Base):
    __tablename__ = 'hisihi_teaching_course_outline'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    teaching_course_id = Column(Integer)
    title = Column(String(50), nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)
