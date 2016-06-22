from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class GiftPackage(Base):
    __tablename__ = 'hisihi_organization_gift_package'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    introduce = Column(String(255), nullable=False)
    detail = Column(String(1000), nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)
