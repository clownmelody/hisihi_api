from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, SmallInteger
from herovii.models.base import Base, db

__author__ = 'yangchujie'


class DocumentArticle(db.Model):

    __tablename__ = 'hisihi_document_article'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    source_name = Column(String(100), nullable=False)
    logo_pic = Column(Integer, nullable=True)
    fake_support_count = Column(Integer, nullable=True)
