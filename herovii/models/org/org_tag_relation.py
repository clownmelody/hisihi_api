from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'shaolei'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class OrgTagRelation(Base):
    __tablename__ = 'hisihi_organization_tag_relation'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer, nullable=False)
    tag_id = Column(Integer, nullable=False)
    tag_type = Column(String(50), nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger)
