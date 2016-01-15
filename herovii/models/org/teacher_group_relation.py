from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from herovii.models.base import Base

__author__ = 'bliss'


class TeacherGroupRelation(Base):
    __tablename__ = 'hisihi_organization_relation'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    teacher_group_id = Column(Integer)
    group = Column(Integer)
    organization_id = Column(Integer)


    def keys(self):
        return (
            'id', 'uid', 'teacher_group_id'
        )