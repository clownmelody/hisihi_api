__author__ = 'bliss'

from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from herovii.models.base import Base


class UserCSUSecure(Base):

    __tablename__ = 'hisihi_ucenter_member'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
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
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
