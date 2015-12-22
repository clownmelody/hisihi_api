import time

__author__ = 'shaolei'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class Feedback(Base):
    __tablename__ = 'hisihi_organization_feedback'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False)
    qq = Column(String(15), nullable=False)
    content = Column(String(500), nullable=False)
    create_time = Column(Integer, nullable=False)
    status = Column(Integer, default=1)

    def __init__(self):
        self.create_time = time.time()
        super(Feedback, self).__init__()
        
    def keys(self):
        return (
            'id', 'organization_id', 'qq',
            'content', 'create_time', 'status'
        )

