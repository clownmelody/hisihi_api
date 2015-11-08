__author__ = 'bliss'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class App(Base):

    __tablename__ = 'app'
    __bind_key__ = 'heroapi'

    id = Column(Integer, primary_key=True)
    app_id = Column(String(100), nullable=False)
    app_secret = Column(String(100), nullable=False)
    description = Column(String(421))
    scope = Column(String(50), nullable=False)