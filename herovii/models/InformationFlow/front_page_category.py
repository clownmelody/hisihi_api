from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'shaolei'


class FrontPageCategory(Base):

    __tablename__ = 'hisihi_front_page_category'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)
