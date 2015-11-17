from flask import current_app
from herovii.models.base import db
from herovii.models.user.user_org import UserOrg
from herovii.models.user.user import User

__author__ = 'bliss'


def get_user_by_uid(uid):
    user = User.query.filter_by(id=uid).first()
    if user:
        return user
    else:
        return None


def register_by_mobile(mobile, password):
    user = UserOrg()
    user.password = password
    user.mobile = mobile
    with db.auto_commit():
        db.session.add(user)
    return user
