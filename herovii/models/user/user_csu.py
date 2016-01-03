__author__ = 'bliss'


from sqlalchemy import Column, Integer, String, Date, CHAR, SmallInteger
from herovii.models.base import BaseNoCreateTime


class UserCSU(BaseNoCreateTime):

    __tablename__ = 'hisihi_member'
    __bind_key__ = 'csu'

    uid = Column(Integer, primary_key=True)
    nickname = Column(String(16), unique=True, nullable=False)
    sex = Column(SmallInteger)
    birthday = Column(Date)
    qq = Column(CHAR(20))
    score = Column(Integer, default=0)
    reg_id = Column(String(32))

    def keys(self):
        return (
            'uid', 'nickname', 'sex'
        )

