from sqlalchemy import Column, Integer, String, SmallInteger
import time
from herovii.models.base import Base

__author__ = 'yangchujie'


class Promotion(Base):
    __tablename__ = 'hisihi_promotion'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    title = Column(String(45), nullable=False)
    logo_url = Column(String(100), nullable=False)
    little_logo_url = Column(String(100), nullable=False)
    tag_url = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    type = Column(Integer, nullable=False, default=1)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)

    def __init__(self, **entries):
        self.__dict__.update(entries)
        super(PromotionClass, self).__init__()

    def keys(self):
        return (
            'id', 'title', 'logo_url', 'little_logo_url', 'tag_url', 'description', 'type'
        )
