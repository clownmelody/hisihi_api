__author__ = 'bliss'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class TeacherGroup(Base):
    __tablename__ = 'teacher_group'
    __bind_key__ = 'org'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    title = Column(String(120), nullable=False)

    def keys(self):
        return (
            'id', 'organization_id', 'title'
        )

