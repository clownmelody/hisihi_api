from sqlalchemy.sql.sqltypes import SmallInteger

__author__ = 'bliss'


from sqlalchemy import Column, Integer, String, Date
from herovii.models.base import Base


class Org(Base):

    __tablename__ = 'Org'
    __bind_key__ = 'org'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    slogan = Column(String(80))
    location = Column(Date)
    lon = String(40)
    lat = String(40)

    # 机构类型，使用#号分隔，内容为Tag表的记录id
    type = String(80)

    # 机构审核进度
    audit_status = Column(SmallInteger, default=0)
    phone_num = Column(String(80))
    chat_id = Column(Integer)
    logo = Column(String(255))
    video = Column(String(255))
    video_img = Column(String(255))

    # 机构优势，一段纯文本，使用#号分隔，只支持覆盖，不支持局部更新
    advantage = Column(String(1000))
    introduce = Column(String(1000))
    pv = Column(Integer, default=0)
    guarantee_num = Column(Integer, default=200)

    def keys(self):
        return (
            'id', 'name', 'slogan', 'location', 'lon', 'lat',
            'phone_num', 'logo', 'video', 'video_img', 'advantage',
            'introduce', 'pv', 'guarantee_num'
        )

