from sqlalchemy import Column, Integer, String, SmallInteger
from herovii.models.base import Base

__author__ = 'bliss'


class StudentClass(Base):
    __tablename__ = 'hisihi_organization_student_class'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)

    organization_id = Column(Integer)
    title = Column(String(300), nullable=False)
    status = Column(SmallInteger, nullable=True, default=1)
    class_start_date = Column(String(45), nullable=False)
    class_end_date = Column(String(45), nullable=False)
    monday = Column(String(20))
    tuesday = Column(String(20))
    wednesday = Column(String(20))
    thursday = Column(String(20))
    friday = Column(String(20))
    saturday = Column(String(20))
    sunday = Column(String(20))

    def __init__(self, **entries):
        self.__dict__.update(entries)
        super(StudentClass, self).__init__()

    def keys(self):
        return (
            'id', 'organization_id', 'title', 'class_start_date', 'class_end_date',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
        )
