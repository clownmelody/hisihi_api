import time

__author__ = 'shaolei'

from sqlalchemy import Column, Integer, String
from herovii.models.base import Base


class UniversityPhotos(Base):
    __tablename__ = 'hisihi_abroad_university_photos'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, nullable=False)
    pic_url = Column(String(255), nullable=False)
    descript = Column(String(100), nullable=True)
    create_time = Column(Integer, nullable=False)
    status = Column(Integer, default=1)

    def __init__(self):
        self.create_time = time.time()
        super(UniversityPhotos, self).__init__()
        
    def keys(self):
        return (
            'id', 'university_id', 'pic_url', 'descript', 'create_time'
        )

