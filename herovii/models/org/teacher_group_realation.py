from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from herovii.models.base import Base

__author__ = 'bliss'


class TeacherGroupRealation(Base):
    __tablename__ = 'teacher_group_realation'
    __bind_key__ = 'org'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    teacher_group_id = Column(Integer)

    def keys(self):
        return (
            'id', 'uid', 'teacher_group_id'
        )