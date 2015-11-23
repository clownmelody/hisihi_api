import datetime
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer
from sqlalchemy.sql.sqltypes import String, Text, SmallInteger
from herovii.models.base import Base

__author__ = 'bliss'


class NewsOrg(Base):
    __tablename__ = 'news'
    __bind_key__ = 'org'

    id = Column(Integer, primary_key=True)
    # organization_id = Column(Integer, default=0)

    # 新闻类型
    tag = Column(String(45))

    # 新闻标题
    title = Column(String(100), nullable=True)
    content = Column(Text)

    # 新闻是否推送到
    # push_to_organization = Column(SmallInteger, default=0)
    update_time = Column(Integer, default=int(datetime.datetime.now().timestamp()))

    def keys(self):
        return (
            'id', 'tag', 'title', 'content',
            'create_time', 'update_time'
        )


