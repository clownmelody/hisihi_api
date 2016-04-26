import time

__author__ = 'shaolei'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class LowPriceFeedback(Base):
    __tablename__ = 'hisihi_user_find_low_price'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False)
    organization_name = Column(String(100), nullable=False)
    course_name = Column(String(100), nullable=False)
    name = Column(String(45), nullable=False)
    phone_num = Column(String(45), nullable=False)
    create_time = Column(Integer, nullable=False)
    status = Column(Integer, default=1)

    def __init__(self):
        self.create_time = time.time()
        super(LowPriceFeedback, self).__init__()
        
    def keys(self):
        return (
            'id', 'organization_id', 'organization_name',
            'course_name', 'name', 'phone_num', 'create_time', 'status'
        )

