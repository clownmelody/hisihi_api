from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from herovii.models.base import BaseMixin, db

__author__ = 'shaolei'


class Field(db.Model, BaseMixin):

    __tablename__ = 'hisihi_field'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    field_id = Column(Integer, nullable=False)
    field_data = Column(String(1000), nullable=False)
    createTime = Column(Integer, nullable=False)
    changeTime = Column(Integer, nullable=False)

    def keys(self):
        return (
            'id', 'uid', 'field_id', 'field_data'
        )
