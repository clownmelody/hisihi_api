

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base
__author__ = 'bliss'


class Issue(Base):
    __tablename__ = 'hisihi_issue'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    title = Column(Integer, nullable=True)
    allow_post = Column(String(50), nullable=True)

    def keys(self):
        return (
            'id', 'title', 'allow_post'
        )