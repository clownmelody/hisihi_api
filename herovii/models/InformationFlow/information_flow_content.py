from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'yangchujie'


class InformationFlowContent(Base):

    __tablename__ = 'hisihi_information_flow_content'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, nullable=False)
    content_type = Column(Integer, nullable=True)
    content_name = Column(String(200), nullable=True)
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)
    config_type = Column(Integer, nullable=True)
    sort = Column(Integer, nullable=True)
