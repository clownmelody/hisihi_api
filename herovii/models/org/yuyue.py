from sqlalchemy import Column, Integer, String, SmallInteger
import time
from herovii.models.base import Base

__author__ = 'yangchujie'


class Yuyue(Base):
    __tablename__ = 'hisihi_organization_yuyue'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    uid = Column(Integer, nullable=False)
    mobile = Column(String(45), nullable=False)
    organization_id = Column(Integer)
    course_id = Column(Integer)
    university_id = Column(Integer)
    status = Column(Integer)

