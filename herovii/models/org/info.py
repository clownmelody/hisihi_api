from sqlalchemy.sql.sqltypes import SmallInteger

__author__ = 'bliss'


from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class Info(Base):

    __tablename__ = 'hisihi_organization'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    name = Column(String(80), nullable=False)
    city = Column(String(80))


    # 宣传语
    slogan = Column(String(80))
    location = Column(String(100))
    longitude = Column(String(40))
    latitude = Column(String(40))

    # 机构类型，使用#号分隔，内容为Tag表的记录id
    type = Column(String(80))

    # 机构审核进度
    application_status = Column(SmallInteger, default=1)
    light_authentication = Column(SmallInteger, default=0)
    phone_num = Column(String(80), nullable=False)
    chat_id = Column(Integer)
    logo = Column(String(255))
    video = Column(String(255))
    video_img = Column(String(255))

    # 机构优势，一段纯文本，使用#号分隔，只支持覆盖，不支持局部更新
    advantage = Column(String(1000))

    # 简介
    introduce = Column(String(1000))
    view_count = Column(Integer, default=0)

    # 剩余担保人数
    guarantee_num = Column(Integer, default=200)

    def __init__(self, **entries):
        self.__dict__.update(entries)
        super(Info, self).__init__()

    def keys(self):
        return (
            'id', 'name', 'slogan', 'location', 'longitude', 'latitude',
            'phone_num', 'logo', 'video', 'video_img', 'advantage',
            'introduce', 'view_count', 'guarantee_num', 'city', 'type'
        )

