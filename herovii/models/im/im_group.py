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
    conversion_id = Column(Integer, nullable=True)
    group_avatar = Column(String(120))
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self, group_name, create_time, organization_id, conversion_id, group_avatar):
        self.group_name = group_name
        self.create_time = create_time
        self.organization_id = organization_id
        self.conversion_id = conversion_id
        self.group_avatar = group_avatar


    def keys(self):
        return (
            'id', 'group_name', 'organization_id', 'conversion_id', 'group_avatar', 'create_time', 'status'
        )