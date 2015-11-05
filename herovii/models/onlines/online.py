__author__ = 'bliss'

import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from herovii.models.base import Base


class Online(Base):

    __tablename__ = 'online'
    __bind_key__ = 'online'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    desc = Column(String(200))
    begin_time = Column(Integer, default=int(datetime.datetime.now().timestamp()))
    end_time = Column(Integer, default=int(datetime.datetime.now().timestamp()))
    related_url = Column(String(300))