__author__ = 'bliss'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class OrgCourse(Base):
    __tablename__ = 'course'
    __bind_key__ = 'org'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    student_uid = Column(Integer)
    student_name = Column(String(30))
    phone_number = Column(String(20))
    student_university = Column(String(50))
    course_id = Column(Integer)

    def keys(self):
        return {
            'id', 'organization_id', 'student_uid', 'student_name',
            'phone_number', 'student_university', 'course_id'
        }

