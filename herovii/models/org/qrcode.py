import datetime
from flask.ext.restful.fields import String
from flask.helpers import url_for
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from herovii.models.base import Base

__author__ = 'bliss'


class OrgQrcodeSignIn(Base):
    """签到二维码，每个机构每天一张"""
    QRCODE_URL = url_for('v1.org+get_qrcode_for_sign_in')
    __tablename__ = 'hisihi_organization_qrcode_sign_in'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    qrcode_url = Column(String(100), nullable=False)
    date = Column(String(50), nullable=False, default=datetime.datetime.now().strftime('%Y-%m-%d'))
    organization_id = Column(Integer, nullable=False)

    def __init__(self):
        OrgQrcodeSignIn.QRCODE_URL +=
        super(OrgQrcodeSignIn, self).__init__()
