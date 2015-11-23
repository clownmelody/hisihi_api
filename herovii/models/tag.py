

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base
__author__ = 'bliss'


class Tag(Base):
    __tablename__ = 'tag'
    __bind_key__ = 'org'

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=True)
    value = Column(String(50), nullable=True)

    def keys(self):
        return (
            'id', 'type', 'value',
            'create_time'
        )