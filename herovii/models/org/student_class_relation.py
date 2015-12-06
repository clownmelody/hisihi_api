from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from herovii.models.base import Base

__author__ = 'bliss'


class StudentClassRelation(Base):
    __tablename__ = 'hisihi_organization_student_class_relation'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    student_class_id = Column(Integer)

    def keys(self):
        return (
            'id', 'uid', 'student_class_id'
        )