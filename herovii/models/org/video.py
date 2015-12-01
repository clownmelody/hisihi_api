import time

__author__ = 'bliss'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class OrgVideo(Base):
    __tablename__ = 'hisihi_organization_video'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    course_id = Column(Integer)
    name = Column(String(120), nullable=False)
    url = Column(String(300))
    duration = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    update_time = Column(Integer)

    def __init__(self):
        self.update_time = time.time()
        super(OrgVideo, self).__init__()
        
    def keys(self):
        return (
            'id', 'course_id', 'name', 'url',
            'duration', 'view_count', 'update_time',
            'create_time'
        )

