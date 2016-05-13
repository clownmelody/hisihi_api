from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer
from herovii.models.base import Base


class OrgAuthentication(Base):
    __tablename__ = 'hisihi_organization_authentication'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    authentication_id = Column(Integer)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)
