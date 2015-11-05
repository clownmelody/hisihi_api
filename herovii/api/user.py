__author__ = 'bliss'

from flask import json, jsonify
from herovii.validator.forms import RegisterByMobileForm
from herovii.service import user_srv, account
from herovii.validator import user_verify
from herovii.libs.error_code import NotFound, UnknownError
from herovii.libs.bpbase import ApiBlueprint
from herovii.handlers.account import auth
from herovii.models.user_org import UserOrg
from herovii.models.base import db
from herovii.libs.httper import BMOB

api = ApiBlueprint('user')
# auth = HTTPBasicAuth()


@api.route('/org', methods=['POST'])
def create_by_mobile():
    """ 添加一个机构用户
    调用此接口需要先调用'/v1/sms/verify' 接口，以获得短信验证码
    :POST:
        {'phone_number':'18699998888', 'sms_code':'876876', 'password':'password'}
    :return:
    """
    bmob = BMOB()
    form = RegisterByMobileForm.create_api_form()
    phone_number = form.phone_number.data
    sms_code = form.sms_code.data
    status, body = bmob.verify_sms_code(phone_number, sms_code)
    if status == 200:
        user = account.register_by_mobile(phone_number, sms_code)
        return jsonify(user), 201
    else:
        j = json.loads(body)
        raise UnknownError(j['error'], error_code=None)


@api.route('/<uid>', methods=['GET'])
@auth.login_required
def get_user_uid(uid):
    uid = user_verify.verify_uid(uid)
    user = user_srv.get_user_by_uid(uid)
    if user:
        return jsonify(user), 200
    else:
        raise NotFound('user not found', 2000)


@api.route('/test', methods=['GET'])
def test():
    # pass
    user = UserOrg()
    user.password = '19851118'
    user.mobile = "18607131949"
    with db.auto_commit():
        db.session.add(user)
    return jsonify(user), 201
