__author__ = 'bliss'

from flask import current_app
from herovii.models.user.user import User
from herovii.models.user.user_org import UserOrgAdmin
from herovii.models.user.user_csu_secure import UserCSUSecure
from herovii.models.base import db
from herovii.libs.error_code import NotFound
from herovii.models.heroapi.app import App
from herovii.libs.helper import check_md5_password


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


def reset_password_by_mobile(mobile, password):
    user = UserOrgAdmin.query.filter_by(mobile=mobile).first()
    if user is not None:
        with db.auto_commit():
            user.update(
                {
                    UserOrgAdmin.password: password
                }
            )
    else:
        raise NotFound(error='user not found', error_code=2000)
    return user


# def verify_by_phone_number(phone_number, password):
#     user = UserOrgAdmin.query.filter_by(mo=phone_number).first()
#     if not user or not user.check_password(password):
#         return None
#     else:
#         return user.id


def verify_in_heroapi(key, secret):
    app = App.query.filter_by(app_id=key, app_secret=secret).first()
    if app is not None:
        return [app.app_key, app.scope]
    else:
        return None


def verify_in_csu_by_social(uuid, secret=None):
    """ 通过uuid or openid 进行授权
    目前Andorid端没有将授权码Code返回服务器进行第三方授权
    而是传递的OpenId。占时只需要使用OpenId或者UUID来进行登录授权。
    极度不安全。后期需要更改为使用code码拉取用户信息的方式验证
    :param uuid: 用户的第三方唯一ID（openid or uuid）
    :return uid: 返回用户在服务器的ID
    """
    uid = db.session.query(UserCSUSecure.id)\
        .filter_by(username=uuid).first()
    if uid:
        return [uid[0], 'UserCSU']
    else:
        return None


def verify_in_csu_by_mobile(mobile, raw_password):
    """通过验证用户手机和密码进行授权"""
    user_csu_secure = db.session.query(UserCSUSecure)\
        .filter_by(mobile=mobile).first()
    if not user_csu_secure:
        return None
    else:
        valid = user_csu_secure.check_password(raw_password)
    if valid:
        return [user_csu_secure.id, 'UserCSU']
    else:
        return None


def verify_in_org_by_mobile(mobile, raw_password):
    """通过验证Org用户的手机和密码进行授权"""
    user_org = UserOrgAdmin.query.filter_by(mobile=mobile).first()
    if user_org.check_password(raw_password):
        return True
    else:
        return False

























