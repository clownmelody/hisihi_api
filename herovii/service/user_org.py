from herovii.models.base import db
from herovii.models.user.user_csu import UserCSU
from herovii.models.user.user_org import OrgAdmin

__author__ = 'bliss'


def get_user_by_uid(uid):
    user = UserCSU.query.filter_by(uid=uid).first()
    if user:
        return user
    else:
        return None


def register_by_mobile(mobile, password):
    user = OrgAdmin()
    user.password = password
    user.mobile = mobile
    with db.auto_commit():
        db.session.add(user)
    return user
