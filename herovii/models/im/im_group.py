from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'yangchujie'


class ImGroup(Base):

    __tablename__ = 'hisihi_im_groups'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    group_name = Column(String(45), nullable=False)
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self, group_name, create_time):
        self.group_name = group_name
        self.create_time = create_time


    def keys(self):
        return (
            'id', 'group_name', 'create_time', 'status'
        )