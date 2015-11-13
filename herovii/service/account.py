__author__ = 'bliss'

from herovii.models.user.user import User
from herovii.models.user.user_org import UserOrg
from herovii.models.user.user_csu_secure import UserCSUSecure
from herovii.models.base import db
from herovii.libs.error_code import NotFound
from herovii.models.heroapi.app import App


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


def register_by_mobile(mobile, password):
    user = UserOrg()
    user.password = password
    user.mobile = mobile
    with db.auto_commit():
        db.session.add(user)
    return user


def reset_password_by_mobile(mobile, password):
    user = UserOrg.query.filter_by(mobile=mobile).first()
    if user is not None:
        with db.auto_commit():
            user.update({UserOrg.password: password})
    else:
        raise NotFound(error='user not found', error_code=2000)
    return user


def verify_by_phone_number(phone_number, password):
    user = UserOrg.query.filter_by(mo=phone_number).first()
    if not user or not user.check_password(password):
        return None
    else:
        return user.id


def verify_in_heroapi(key, secret):
    app = App.query.filter_by(app_id=key, app_secret=secret).first()
    if app is not None:
        return app.scope
    else:
        return None


def verify_in_csu_by_social(uuid):
    """
    目前Andorid端没有将授权码Code返回服务器进行第三方授权
    而是传递的OpenId。占时只需要使用OpenId或者UUID来进行登录授权。
    极度不安全。后期需要更改为使用code码拉取用户信息的方式验证
    :param uuid: 用户的第三方唯一ID（openid or uuid）
    :return uid: 返回用户在服务器的ID
    """
    uid = db.session.query(UserCSUSecure.id)\
        .filter_by(user_name=uuid).first()
    if uid:
        return uid
    else:
        return None

























