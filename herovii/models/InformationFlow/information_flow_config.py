from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'yangchujie'


class InformationFlowConfig(Base):

    __tablename__ = 'hisihi_information_flow_config'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    title = Column(String(45), nullable=False)
    create_time = Column(Integer)
    update_time = Column(Integer)
    status = Column(SmallInteger, default=1)
