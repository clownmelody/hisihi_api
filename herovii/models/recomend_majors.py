from sqlalchemy import Column, Integer, String
from herovii.models.base import Base
__author__ = 'yangchujie'


class RecomendMajors(Base):
    __tablename__ = 'hisihi_recomend_majors'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    sort = Column(Integer, nullable=True)
    create_time = Column(Integer)
    status = Column(Integer, default=1)

    def keys(self):
        return (
            'id', 'name', 'sort'
        )