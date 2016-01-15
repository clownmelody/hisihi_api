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
    web_name = Column(String(15))

    # 网址链接
    url = Column(String(100))

    # 图标地址
    icon_url = Column(String(100))

    # 所属类别
    class_id = Column(Integer)

    # 推荐状态,默认值为1，表示不推荐
    state = Column(SmallInteger)

    # 访问量:真实和虚假
    real_score = Column(Integer)
    fake_score = Column(Integer)

    def __init__(self):
        self.status = 1

    def keys(self):
        return (
            'id', 'web_name', 'url', 'icon_url',
            'class_id', 'state', 'real_score', 'fake_score'
        )


