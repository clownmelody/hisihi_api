from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'shaolei'


class FrontPage(Base):

    __tablename__ = 'hisihi_front_page'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    article_title = Column(String(100), nullable=False)
    category = Column(Integer, nullable=False)
    article_id = Column(Integer, nullable=False)
    source_name = Column(String(50), nullable=True)
    cover_id = Column(Integer, nullable=True)
    article_format = Column(Integer, nullable=True)
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)
