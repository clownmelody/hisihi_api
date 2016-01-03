import datetime
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
import time
from herovii.models.base import Base

__author__ = 'yangchujie'


class ClassPushHistory(Base):
    __tablename__ = 'hisihi_organization_class_push_history'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, nullable=False)
    date = Column(String(45), nullable=False)
    create_time = Column(Integer)

    def __init__(self, class_id):
        self.class_id = class_id
        self.date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.create_time = int(datetime.datetime.now().timestamp())
        self.status = 1

    def keys(self):
        return (
            'id', 'class_id', 'date', 'status'
        )