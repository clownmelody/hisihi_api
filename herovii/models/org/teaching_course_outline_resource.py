from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class TeachingCourseOutlineResource(Base):
    __tablename__ = 'hisihi_teaching_course_outline_resource'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    outline_id = Column(Integer)
    name = Column(String(50), nullable=False)
    type = Column(Integer)
    video_id = Column(Integer)
    cover_pic = Column(String(100), nullable=True)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)
