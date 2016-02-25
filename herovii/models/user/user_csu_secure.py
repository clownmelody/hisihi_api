from herovii.libs.helper import check_md5_password

__author__ = 'bliss'

from sqlalchemy import Column, Integer, String
from herovii.models.base import BaseNoCreateTime


class UserCSUSecure(BaseNoCreateTime):

    __tablename__ = 'hisihi_ucenter_member'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    _password = Column('password', String(80), nullable=False)
    email = Column(String(50), unique=True)
    mobile = Column(String(20), unique=True)

    def keys(self):
        return (
            # 'id', 'username', 'mobile',
            # 'create_time'
        )

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        from herovii.libs.helper import secret_password
        if raw is not None or '':
            self._password = secret_password(raw)
        # self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_md5_password(self._password, raw)
