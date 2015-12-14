from sqlalchemy import Column, Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'bliss'


class StudentClass(Base):
    __tablename__ = 'hisihi_organization_student_class'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    title = Column(String(300), nullable=False)
    status = Column(SmallInteger, nullable=True)

    def keys(self):
        return (
            'id', 'organization_id', 'title', 'status'
        )
