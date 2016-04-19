from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'yangchujie'


class Document(Base):

    __tablename__ = 'hisihi_document'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    category_id = Column(Integer, nullable=True)
    description = Column(String(140), nullable=False)
    position = Column(Integer, nullable=True)
    cover_id = Column(Integer, nullable=True)
    view = Column(Integer, nullable=True)
    cover_id = Column(Integer, nullable=True)
    cover_type = Column(Integer, nullable=True)
    create_time = Column(Integer)
    update_time = Column(Integer)
    status = Column(SmallInteger, default=1)
