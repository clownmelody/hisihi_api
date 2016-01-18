from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'yangchujie'


class ImGroup(Base):

    __tablename__ = 'hisihi_im_groups'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    group_name = Column(String(45), nullable=False)
    organization_id = Column(Integer, nullable=True)
    conversation_id = Column(String(100), nullable=True)
    group_avatar = Column(String(120))
    description = Column(String(300))
    create_time = Column(Integer)
    level = Column(Integer, default=1000)
    status = Column(SmallInteger, default=1)

    def __init__(self, group_name, create_time, organization_id, conversation_id, group_avatar, description):
        self.group_name = group_name
        self.create_time = create_time
        self.organization_id = organization_id
        self.conversation_id = conversation_id
        self.group_avatar = group_avatar
        self.description = description


    def keys(self):
        return (
            'id', 'group_name', 'organization_id', 'conversation_id', 'group_avatar', 'create_time', 'status'
        )