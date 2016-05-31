from sqlalchemy.sql.sqltypes import SmallInteger
import time

__author__ = 'shaolei'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class OrgAdminBindWeixin(Base):
    __tablename__ = 'hisihi_organization_admin_bind_weixin'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer)
    weixin_account = Column(String(100), nullable=False)
    weixin_nickname = Column(String(100), nullable=False)
    weixin_avatar = Column(String(255), nullable=False)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger, default=1)

    def __init__(self, **entries):
        self.__dict__.update(entries)
        super(OrgAdminBindWeixin, self).__init__()

    def keys(self):
        return (
            'id', 'admin_id', 'weixin_account', 'weixin_nickname', 'weixin_avatar'
        )