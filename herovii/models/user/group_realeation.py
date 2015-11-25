from sqlalchemy import Column, Integer, String
from herovii.models.base import BaseNoCreateTime

__author__ = 'bliss'


class Group(BaseNoCreateTime):

    __tablename__ = 'hisihi_auth_group_access'
    __bind_key__ = 'csu'

    uid = Column(Integer)
    group_id = Column(Integer)

    def keys(self):
        return (
            'uid', 'group_id', 'description'
        )