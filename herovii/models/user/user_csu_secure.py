__author__ = 'bliss'

import hashlib
from sqlalchemy import Column, Integer, String, Boolean
from herovii.models.base import BaseNoCreateTime


class UserCSUSecure(BaseNoCreateTime):

    __tablename__ = 'hisihi_ucenter_member'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    _password = Column('password', String(80), nullable=False)
    email = Column(String(50), unique=True)
    mobile = Column(String(20), unique=True)

    status = Column(Boolean)

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
        from flask import current_app
        self._password = secret_password(raw, current_app.config['USER_CSU_PSW_SALT'])
        # self._password = generate_password_hash(raw)
