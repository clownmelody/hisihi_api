from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer
from sqlalchemy.sql.sqltypes import String, SmallInteger
from herovii.models.base import Base

__author__ = 'melody'


class Yellow(Base):
    __tablename__ = 'hisihi_yellow_pages'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    # 网站名称
    website_name = Column(String(40))

    # 网址链接
    url = Column(String)

    # 图标地址
    icon_url = Column(String)

    # 所属类别
    class_id = Column(Integer)

    # 黄页标签id
    label = Column(Integer)

    # 访问量:真实和虚假
    real_view_count = Column(Integer)
    fake_view_count = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.label = 0
        self.real_score = 0
        self.fake_score = 0
        self.status = 1

    def keys(self):
        return (
            'id', 'website_name', 'url', 'icon_url',
            'class_id', 'label', 'real_view_count', 'fake_view_count'
        )


