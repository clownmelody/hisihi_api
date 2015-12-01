import datetime
from flask.helpers import url_for
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from herovii.libs.helper import make_a_qrcode
from herovii.models.base import Base
from herovii.service.file import FilePiper

__author__ = 'bliss'


class QrcodeSignIn(Base):
    """签到二维码，每个机构每天一张"""
    __tablename__ = 'hisihi_organization_qrcode_sign_in'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    qrcode_url = Column(String(100), nullable=False)
    date = Column(String(50), nullable=False)
    organization_id = Column(Integer, nullable=False)
    oss_url = Column(String(100), nullable=False)

    def __init__(self, oid, date):
        self.date = date.strftime('%Y-%m-%d')
        self.organization_id = oid
        super(QrcodeSignIn, self).__init__()

    def keys(self):
        return (
            'id', 'qrcode_url', 'date', 'organization_id',
            'oss_url'
        )

    def make(self):
        param = {
            'oid': self.organization_id,
            'uid': 0,
            'date': self.date
        }
        self.qrcode_url = url_for('.student_sign_in', **param)
        self.oss_url = self.__create_qrcode()
        return self.oss_url

    def __create_qrcode(self):
        f = make_a_qrcode(self.qrcode_url)
        oss_url = FilePiper.upload_bytes_to_oss(f)
        return oss_url
