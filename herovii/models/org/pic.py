from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import SmallInteger
from herovii.models.base import Base
__author__ = 'bliss'


class OrgPic(Base):
    __tablename__ = 'pic'
    __bind_key__ = 'org'

    id = Column(Integer, primary_key=True)
    uri = Column(String(120))
    description = Column(String(300))
    type = Column(SmallInteger)

    organization_id = Column(Integer, nullable=False)

    def keys(self):
        return (
            'id', 'organization_id', 'uri',
            'description', 'type'
        )

