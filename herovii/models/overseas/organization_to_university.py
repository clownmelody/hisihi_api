import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer
from herovii.models.base import Base


class OrganizationToUniversity(Base):
    __tablename__ = 'hisihi_organization_to_university'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False)
    teaching_course_id = Column(Integer, nullable=False)
    university_id = Column(Integer, nullable=False)
    create_time = Column(Integer, nullable=False)
    status = Column(Integer, default=1)

    def __init__(self):
        self.create_time = time.time()
        super(OrganizationToUniversity, self).__init__()
        
    def keys(self):
        return (
            'id', 'organization_id', 'teaching_course_id',
            'university_id', 'create_time', 'status'
        )

