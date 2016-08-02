from herovii.libs.helper import check_md5_password

__author__ = 'shaolei'

from sqlalchemy import Column, Integer, String
from herovii.models.base import BaseNoCreateTime


class UserStatsSecure(BaseNoCreateTime):

    __tablename__ = 'account'
    __bind_key__ = 'stats'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    _password = Column('password', String(80), nullable=False)


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
        else:
            if self._password == raw:
                return True
            else:
                return False
        """原始密码同md5加密的密码进行校验"""
        # return check_md5_password(self._password, raw)
