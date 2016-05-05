import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class Country(Base):
    __tablename__ = 'hisihi_abroad_country'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    logo_url = Column(String(100), nullable=False)
    is_hot = Column(Integer, nullable=False)
    create_time = Column(Integer, nullable=False)
    status = Column(Integer, default=1)

    def __init__(self):
        self.create_time = time.time()
        super(Country, self).__init__()
        
    def keys(self):
        return (
            'id', 'name', 'logo_url',
            'is_hot', 'create_time', 'status'
        )

