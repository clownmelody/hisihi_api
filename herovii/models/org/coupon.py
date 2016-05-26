from sqlalchemy import Column, Integer, String, SmallInteger
import time
from herovii.models.base import Base

__author__ = 'yangchujie'


class Coupon(Base):
    __tablename__ = 'hisihi_coupon'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    name = Column(String(45), nullable=False)
    type = Column(Integer, nullable=False, default=1)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    service_condition = Column(String(200), nullable=False)
    using_method = Column(String(200), nullable=False)
    instructions_for_use = Column(String(200), nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)

    def __init__(self, **entries):
        self.__dict__.update(entries)
        super(Coupon, self).__init__()

    def keys(self):
        return (
            'id', 'name', 'start_time', 'end_time', 'money', 'type'
        )
