from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class OrgAuthenticationConfig(Base):
    __tablename__ = 'hisihi_organization_authentication_config'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    name = Column(String(50))
    default_display = Column(Integer)
    pic_url = Column(String(50))
    disable_pic_url = Column(String(50))
    tag_pic_url = Column(String(50))
    content = Column(String(500))
    flag = Column(Integer)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)
