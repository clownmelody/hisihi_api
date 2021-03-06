from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import SmallInteger
from herovii.models.base import Base
__author__ = 'bliss'


class Pic(Base):
    __tablename__ = 'hisihi_organization_resource'
    __bind_key__ = 'csu'

    TYPE_STUDENT = 1
    TYPE_ENVIRONMENT = 2

    id = Column(Integer, primary_key=True)
    url = Column(String(120))
    description = Column(String(300))
    type = Column(SmallInteger)
    author_avatar = Column(String(100))
    author_name = Column(String(100))
    author_company = Column(String(100))

    organization_id = Column(Integer, nullable=False)

    def keys(self):
        return (
            'id', 'organization_id', 'url',
            'description', 'type', 'author_avatar', 'author_name', 'author_company'
        )

