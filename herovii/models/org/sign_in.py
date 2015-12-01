from sqlalchemy import Column, String, Integer
import time
from herovii.models.base import Base

__author__ = 'bliss'


class StudentSignIn(Base):
    __tablename__ = 'hisihi_organization_sign_in'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    organization_id = Column(Integer)
    sign_in_time = Column(Integer)
    date = Column(String(30))
    
    def __init__(self):
        self.sign_in_time = int(time.time())
        super(StudentSignIn, self).__init__()

    def keys(self):
        return (
            'id', 'uid', 'organization_id', 'sign_in_time',
            'date'
        )
