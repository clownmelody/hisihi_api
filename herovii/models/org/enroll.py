__author__ = 'bliss'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class Enroll(Base):
    __tablename__ = 'hisihi_organization_enroll'
    __bind_key__ = 'csu'

    STATUS_ENROLL_SUCCESS = 2
    STATUS_ENROLL_WAITING = 1
    STATUS_ENROLL_REJECT = -2

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    student_uid = Column(Integer)
    student_name = Column(String(30))
    phone_number = Column(String(20))
    student_university = Column(String(50))
    course_id = Column(Integer)
    confirm_time = Column(Integer)
    blz_id = Column(String(30))

    def keys(self):
        return {
            'id', 'organization_id', 'student_uid', 'student_name',
            'phone_number', 'student_university', 'course_id', 'confirm_time',
            'blz_id'
        }

