__author__ = 'bliss'


from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class UserCSUCreditDynamic(Base):

    __tablename__ = 'hisihi_credit_dynamic'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)

    # 本次积分变化
    credit_dynamic = Column(Integer)

    # 本次积分变化后剩余分数
    left_credit = Column(Integer)
    reason = Column(String(255))
    party = Column(String(50))

    def keys(self):
        return (

        )

