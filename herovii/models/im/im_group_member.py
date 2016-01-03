from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'yangchujie'


class ImGroupMember(Base):

    __tablename__ = 'hisihi_im_group_members'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False)
    member_id = Column(String(45), nullable=False)
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)
    is_admin = Column(SmallInteger, default=0)

    def __init__(self, group_id, member_id, create_time, is_admin=0):
        self.group_id = group_id
        self.member_id = member_id
        self.create_time = create_time
        self.is_admin = is_admin

    def keys(self):
        return (
            'id', 'group_id', 'member_id', 'create_time', 'status'
        )