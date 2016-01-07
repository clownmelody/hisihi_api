from sqlalchemy import Column, Integer, String
from herovii.models.base import Base
__author__ = 'bliss'


class TeacherGroup(Base):
    __tablename__ = 'hisihi_organization_lecture_group'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    title = Column(String(120), nullable=False)

    def keys(self):
        return (
            'id', 'organization_id', 'title'
        )

