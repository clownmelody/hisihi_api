__author__ = 'bliss'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class StatisticEx(Base):
    __tablename__ = 'statistic_ex'
    __bind_key__ = 'online'

    id = Column(Integer, primary_key=True)
    f_online_id = Column(Integer, nullable=False)
    key = Column(String(20), nullable=False, unique=True)
    value = Column(String(50), nullable=False)