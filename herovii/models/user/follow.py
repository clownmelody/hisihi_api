from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from herovii.models.base import BaseMixin, db
import time
__author__ = 'shaolei'


class Follow(db.Model, BaseMixin):

    __tablename__ = 'hisihi_follow'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    follow_who = Column(Integer, nullable=False)
    who_follow = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False, default=1)
    create_time = Column(Integer, nullable=False, default=int(time.time()))

    def keys(self):
        return (
            'id', 'follow_who', 'who_follow', 'type'
        )
