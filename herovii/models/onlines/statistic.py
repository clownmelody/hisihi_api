__author__ = 'bliss'

import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from herovii.models.base import Base


class Statistic(Base):

    __tablename__ = 'statistic'
    __bind_key__ = 'online'

    id = Column(Integer, primary_key=True)
    f_online_id = Column(Integer, nullable=False)
    pv = Column(Integer, default=0)
    uv = Column(Integer, default=0)
    iphone_downloads = Column(Integer, default=0)
    android_downloads = Column(Integer, default=0)
    ipad_downloads = Column(Integer, default=0)
    other_downloads = Column(Integer, default=0)
