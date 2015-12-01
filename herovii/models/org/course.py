from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'bliss'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class Course(Base):
    __tablename__ = 'hisihi_organization_course'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    title = Column(String(300), nullable=False)
    content = Column(String(500))
    img = Column(String(300))
    category_id = Column(Integer)
    lecture = Column(Integer)
    auth = Column(SmallInteger, default=1)
    view_count = Column(Integer, default=0)
    update_time = Column(Integer, default=int(time.time()))


    def keys(self):
        return (
            'id', 'organization_id', 'title'
        )

