from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from herovii.models.base import Base

__author__ = 'bliss'


class Classmate(Base):
    __tablename__ = 'hisihi_organization_student_classmate'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    class_id = Column(Integer)
    status = Column(Integer, default=1)

    def keys(self):
        return (
            'id', 'uid', 'student_class_id'
        )
