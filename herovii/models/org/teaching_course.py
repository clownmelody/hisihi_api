import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class TeachingCourse(Base):
    __tablename__ = 'hisihi_organization_teaching_course'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    course_name = Column(String(100))
    cover_pic = Column(String(100))
    start_course_time = Column(String(45))
    lesson_period = Column(Integer)
    student_num = Column(Integer)
    lecture_name = Column(String(45))
    introduction = Column(String(500))
    plan = Column(String(400))
    price = Column(Integer)
    already_registered = Column(Integer, default=0)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(Integer, default=1)

    def keys(self):
        return (
            'id', 'organization_id', 'course_name', 'cover_pic', 'price', 'introduction', 'plan',
            'start_course_time', 'lesson_period', 'student_num', 'lecture_name', 'already_registered',
            'create_time', 'status'
        )

