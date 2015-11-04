__author__ = 'bliss'

from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from .base import Base


class UserOrg(Base):

    __tablename__ = 'user_org'

    id = Column(Integer, primary_key=True)
    username = Column(String(45), unique=True)
    email = Column(String(50), unique=True)
    mobile = Column(String(15), unique=True, nullable=False)

    _password = Column('password', String(100))
    organization_id = Column(Integer, unique=True)
    status = Column(Boolean)

    def keys(self):
        return (
            'id', 'username', 'mobile',
            'create_time'
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
