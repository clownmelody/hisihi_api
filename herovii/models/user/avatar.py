from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from herovii.models.base import Base

__author__ = 'bliss'


class Avatar(Base):

    __tablename__ = 'hisihi_avatar'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    path = Column(String(100), nullable=False)

    is_temp = Column(Integer, default=0)

    def keys(self):
        return (
            'id', 'uid', 'path', 'is_temp'
        )