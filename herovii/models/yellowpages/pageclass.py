from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer
from sqlalchemy.sql.sqltypes import String
from herovii.models.base import Base

__author__ = 'melody'


class Category(Base):
    __tablename__ = 'hisihi_page_class'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    # 分类名称
    category_name = Column(String(15))

    # 图标地址
    icon_url = Column(String(100))

    def __init__(self):
        self.status = 1

    def keys(self):
        return (
            'id', 'category_name', 'icon_url'
        )


