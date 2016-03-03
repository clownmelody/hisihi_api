from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'yangchujie'


class InformationFlowBanner(Base):

    __tablename__ = 'hisihi_information_flow_banner'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    pic_url = Column(String(100), nullable=False)
    pic_id = Column(Integer, nullable=True)
    url = Column(String(200), nullable=True)
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)
