from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from herovii.models.base import Base

__author__ = 'bliss'


class StudentClassStats(Base):
    __tablename__ = 'hisihi_organization_student_class_relation'
    __bind_key__ = 'csu'

    TYPE_MEMBER_COUNT = 1

    id = Column(Integer, primary_key=True)
    value = Column(Integer, default=0)
    student_class_id = Column(Integer)
    type = Column(Integer)

    def keys(self):
        return (
            'id', 'uid', 'student_class_id'
        )