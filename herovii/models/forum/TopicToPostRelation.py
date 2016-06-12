__author__ = 'yangchujie'

import time
from sqlalchemy import Column, Integer
from herovii.models.base import Base


class TopicToPostRelation(Base):
    __tablename__ = 'hisihi_forum_topic_to_post_relation'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, nullable=False)
    post_id = Column(Integer, nullable=False)
    create_time = Column(Integer, nullable=False)
    status = Column(Integer, default=1)

    def __init__(self):
        self.create_time = time.time()
        super(TopicToPostRelation, self).__init__()

    def keys(self):
        return (
            'id', 'topic_id', 'post_id', 'create_time', 'status'
        )
