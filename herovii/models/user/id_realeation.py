from sqlalchemy import Column, Integer, Index
from herovii.models.base import BaseNoCreateTime

__author__ = 'bliss'


class IdRelation(BaseNoCreateTime):

    __tablename__ = 'hisihi_auth_group_access'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    uid = Column(Integer)
    group_id = Column(Integer)
    # uid_group = Index("some_index", uid, group_id)

    def keys(self):
        return (
            'uid', 'group_id'
        )
