import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class University(Base):
    __tablename__ = 'hisihi_abroad_university'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    logo_url = Column(String(100), nullable=False)
    website = Column(Integer, nullable=False)
    introduction = Column(String(500), nullable=False)
    sia_recommend_level = Column(String(45), nullable=False)
    sia_student_enrollment_rate = Column(String(45), nullable=False)
    difficulty_of_application = Column(String(45), nullable=False)
    tuition_fees = Column(String(45), nullable=False)
    toefl = Column(String(45), nullable=False)
    ielts = Column(String(45), nullable=False)
    proportion_of_undergraduates = Column(String(45), nullable=False)
    scholarship = Column(String(45), nullable=False)
    deadline_for_applications = Column(String(45), nullable=False)
    application_requirements = Column(String(500), nullable=False)
    school_environment = Column(String(500), nullable=False)
    is_hot = Column(Integer, nullable=False)
    country_id = Column(Integer, nullable=False)
    undergraduate_majors = Column(String(300), nullable=False)
    graduate_majors = Column(String(300), nullable=False)
    create_time = Column(Integer, nullable=False)
    status = Column(Integer, default=1)

    def __init__(self):
        self.create_time = time.time()
        super(University, self).__init__()
        
    def keys(self):
        return (
            'id', 'name', 'logo_url', 'website', 'introduction', 'sia_recommend_level', 'sia_student_enrollment_rate',
            'difficulty_of_application', 'tuition_fees', 'toefl', 'toefl', 'proportion_of_undergraduates',
            'scholarship', 'deadline_for_applications', 'application_requirements', 'school_environment',
            'is_hot', 'country_id', 'undergraduate_majors', 'graduate_majors', 'create_time', 'status'
        )

