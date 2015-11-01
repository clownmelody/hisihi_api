__author__ = 'bliss'

from herovii.models.user import User


def get_user_by_uid(uid):
    user = User.query.filter_by(id=uid).first()
    if user:
        return user
    else:
        return None
