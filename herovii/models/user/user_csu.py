__author__ = 'bliss'


from sqlalchemy import Column, Integer, String, Boolean, Date, CHAR, SmallInteger
from herovii.models.base import BaseNoCreateTime


class UserCSU(BaseNoCreateTime):

    __tablename__ = 'hisihi_member'
    __bind_key__ = 'csu'

    uid = Column(Integer, primary_key=True)
    nickname = Column(String(16), unique=True, nullable=False)
    sex = Column(SmallInteger, nullable=False)
    birthday = Column(Date, nullable=False)
    qq = Column(CHAR(20))
    score = Column(Integer, default=0, nullable=False)

    status = Column(Boolean)

    def keys(self):
        return (
            'uid', 'nickname', 'sex',
            'create_time'
        )

