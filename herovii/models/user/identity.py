from sqlalchemy import Column, Integer, String, Date, CHAR, SmallInteger
from herovii.models.base import BaseNoCreateTime

__author__ = 'bliss'


class Identity(BaseNoCreateTime):

    __tablename__ = 'hisihi_auth_group'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(50))

    def keys(self):
        return (
            'id', 'title'
        )