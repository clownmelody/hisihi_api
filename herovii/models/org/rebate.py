from sqlalchemy import Column, Integer, String, SmallInteger
import time
from herovii.models.base import Base

__author__ = 'yangchujie'


class Rebate(Base):
    __tablename__ = 'hisihi_rebate'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    name = Column(String(45), nullable=False)
    value = Column(Integer, nullable=False, default=1)
    rebate_value = Column(Integer, nullable=False)
    use_start_time = Column(Integer, nullable=False)
    use_end_time = Column(Integer, nullable=False)
    buy_end_time = Column(Integer, nullable=False)
    use_condition = Column(String(200), nullable=False)
    use_method = Column(String(200), nullable=False)
    use_instruction = Column(String(200), nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)

    def __init__(self, **entries):
        self.__dict__.update(entries)
        super(Rebate, self).__init__()

    def keys(self):
        return (
            'id', 'name', 'value', 'rebate_value'
        )
