from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer
from sqlalchemy.sql.sqltypes import String
from herovii.models.base import Base

__author__ = 'shaolei'


class YellowLabel(Base):
    __tablename__ = 'hisihi_yellow_pages_label'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    # 标签名称
    name = Column(String(40))

    # 图标地址
    url = Column(String)

    def keys(self):
        return (
            'id', 'name', 'url'
        )


