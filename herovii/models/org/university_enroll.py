import time

__author__ = 'shaolei'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class UniversityEnroll(Base):
    __tablename__ = 'hisihi_organization_university_enroll'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    university_id = Column(Integer)
    uid = Column(Integer)
    student_name = Column(String(100))
    student_phone_num = Column(String(45))
    student_education = Column(String(45))
    student_qq = Column(String(45))
    study_abroad_purpose = Column(String(100))
    apply_major = Column(String(100))
    create_time = Column(Integer, default=int(time.time()))
    status = Column(Integer, default=1)

    def keys(self):
        return (
            'id', 'university_id', 'uid', 'student_name', 'student_phone_num', 'student_education', 'student_qq',
            'create_time', 'status', 'study_abroad_purpose', 'apply_major'
        )

