from herovii.libs.helper import secret_password, check_md5_password

__author__ = 'bliss'

from sqlalchemy import Column, Integer, String, Boolean
from herovii.models.base import Base


class OrgAdmin(Base):

    __tablename__ = 'hisihi_organization_admin'
    __bind_key__ = 'csu'

    id = Column(Integer, primary_key=True)
    username = Column(String(45), unique=True)
    email = Column(String(50), unique=True)
    mobile = Column(String(15), unique=True, nullable=False)

    _password = Column('password', String(100))
    # organization_id = Column(Integer, unique=True)

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
        self._password = secret_password(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_md5_password(self._password, raw)
