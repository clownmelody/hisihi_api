import time

__author__ = 'yangchujie'

from sqlalchemy import Column, Integer, String, TEXT
from herovii.models.base import Base


class OverseasPlan(Base):
    __tablename__ = 'hisihi_overseas_plan'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False)
    html_content = Column(TEXT, nullable=False)
    url = Column(String, nullable=False)
    create_time = Column(Integer, nullable=False)
    status = Column(Integer, default=1)

    def __init__(self):
        self.create_time = time.time()
        super(OverseasPlan, self).__init__()
        
    def keys(self):
        return (
            'id', 'organization_id', 'html_content',
            'url', 'create_time', 'status'
        )

