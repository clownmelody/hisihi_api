from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import SmallInteger
from herovii.models.base import Base
__author__ = 'bliss'


class OrgPic(Base):
    __tablename__ = 'hisihi_organization_resource'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    url = Column(String(120))
    description = Column(String(300))
    type = Column(SmallInteger)

    organization_id = Column(Integer, nullable=False)

    def keys(self):
        return (
            'id', 'organization_id', 'url',
            'description', 'type'
        )

