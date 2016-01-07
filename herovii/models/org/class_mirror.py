from sqlalchemy import Column, String, Integer
import time
from sqlalchemy.sql.sqltypes import Text
from herovii.models.base import Base

__author__ = 'bliss'


class ClassMirror(Base):
    __tablename__ = 'hisihi_organization_class_mirror'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer)
    classmates = Column(Text())
    organization_id = Column(Integer)

    date = Column(String(30))

    def keys(self):
        return (
            'id', 'classmates', 'organization_id', 'date'
        )
