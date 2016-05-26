import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, SmallInteger, String
from herovii.models.base import Base


class UserGiftPackage(Base):
    __tablename__ = 'hisihi_user_gift_package'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, unique=True)
    obtain_coupon_record_id = Column(Integer)
    name = Column(String)
    phone_num = Column(String)
    address = Column(String)
    create_time = Column(Integer, default=int(time.time()))
    status = Column(SmallInteger, default=1)

    def keys(self):
        return (
            'id', 'uid', 'obtain_coupon_record_id', 'name', 'phone_num', 'address'
        )