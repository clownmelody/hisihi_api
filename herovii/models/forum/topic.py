__author__ = 'yangchujie'
import time
from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class Topic(Base):
    __tablename__ = 'hisihi_forum_topic'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(300), nullable=False)
    img_url = Column(String(100), nullable=False)
    is_hot = Column(Integer, nullable=False)
    create_time = Column(Integer, nullable=False)
    status = Column(Integer, default=1)

    def __init__(self):
        self.create_time = time.time()
        super(Topic, self).__init__()

    def keys(self):
        return (
            'id', 'title', 'description', 'img_url'
            'is_hot', 'create_time', 'status'
        )

