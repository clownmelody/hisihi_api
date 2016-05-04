import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class TeachingCourseEnroll(Base):
    __tablename__ = 'hisihi_organization_teaching_course_enroll'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    course_id = Column(Integer)
    uid = Column(Integer)
    student_name = Column(String(100))
    student_phone_num = Column(String(45))
    student_university = Column(String(100))
    student_qq = Column(String(45))
    create_time = Column(Integer, default=int(time.time()))
    status = Column(Integer, default=1)

    def keys(self):
        return (
            'id', 'course_id', 'uid', 'student_name', 'student_phone_num', 'student_university', 'student_qq',
            'create_time', 'status'
        )

