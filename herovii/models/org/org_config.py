from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class OrgConfig(Base):
    __tablename__ = 'hisihi_organization_config'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    type = Column(Integer)
    value = Column(String(50), nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)
