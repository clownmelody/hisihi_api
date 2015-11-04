__author__ = 'bliss'

from herovii.models.user import User
from herovii.models.user_org import UserOrg
from herovii.models.base import db


def register_by_email(username, email, password):
    user = User(
        username=username,
        email=email
    )

    user.password = password
    user.role = User.ROLE_ACTIVE
    with db.auto_commit():
        db.session.add(user)
    return user


def register_by_mobile(phone_number, password):
    user = UserOrg()
    user.password = password
    user.mobile = phone_number
    with db.auto_commit():
        db.session.add(user)
    return user


def verify_by_phonenumber(phonenumber, password):
    user = User.query.filter_by(username=phonenumber).first()
    if not user or not user.check_password(password):
        return None
    else:
        return user.id

