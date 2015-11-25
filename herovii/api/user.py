from herovii.models.user.user_csu_secure import UserCSUSecure
from herovii.service.user_org import register_by_mobile
from flask import json, jsonify
from herovii.validator.forms import RegisterByMobileForm, PhoneNumberForm
from herovii.service import user_org, account
from herovii.validator import user_verify
from herovii.libs.error_code import NotFound, UnknownError
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.bpbase import auth
from herovii.libs.httper import BMOB
from herovii.libs.helper import success_json

__author__ = 'bliss'

api = ApiBlueprint('user')


@api.route('/csu', methods=['POST'])
def create_csu_user():
    pass


@api.route('/org/admin', methods=['POST'])
def create_org_admin():
    """ 添加一个机构用户
    调用此接口需要先调用'/v1/sms/verify' 接口，以获得短信验证码
    :POST:
        {'phone_number':'18699998888', 'sms_code':'876876', 'password':'password'}
    :return:
    """
    bmob = BMOB()
    form = RegisterByMobileForm.create_api_form()
    phone_number = form.mobile.data
    password = form.password.data
    sms_code = form.sms_code.data
    status, body = bmob.verify_sms_code(phone_number, sms_code)
    if status == 200:
        user = register_by_mobile(phone_number, password)
        return jsonify(user), 201
    else:
        j = json.loads(body)
        raise UnknownError(j['error'], error_code=None)


@api.route('/org/admin', methods=['GET'])
def get_org_admin():
    pass


@api.route('/org/admin', methods=['PUT'])
def get_org_admin():
    pass


@api.route('/password', methods=['PUT'])
def find_user_password():
    """ 重置/找回密码
        调用此接口需要先调用'/v1/sms/verify' 接口，以获得短信验证码
    :PUT:
        {"phone_number":'18699998888', "sms_code":'876876', "password":'password'}
    :return:
    """
    bmob = BMOB()
    form = RegisterByMobileForm.create_api_form()
    mobile = form.phone_number.data
    password = form.password.data
    sms_code = form.sms_code.data
    status, body = bmob.verify_sms_code(mobile, sms_code)
    if status == 200:
        account.reset_password_by_mobile(mobile, password)
        return success_json(), 202
    else:
        j = json.loads(body)
        raise UnknownError(j['error'], error_code=None)


@api.route('/group', methods=["PUT"])
@auth.login_required
def change_group():
    """改变用户操作组"""
    bmob = BMOB()
    form = RegisterByMobileForm.create_api_form()
    phone_number = form.mobile.data
    password = form.password.data
    sms_code = form.sms_code.data
    status, body = bmob.verify_sms_code(phone_number, sms_code)
    if status == 200:
        user = register_by_mobile(phone_number, password)
        return jsonify(user), 201
    else:
        j = json.loads(body)
        raise UnknownError(j['error'], error_code=None)


@api.route('/csu', methods=['GET'])
@auth.login_required
def get_csu():
    form = PhoneNumberForm.create_api_form()
    mobile = form.mobile.data
    user = UserCSUSecure.query.filter_by(mobile=mobile).first_or_404()
    return jsonify(user), 200


@api.route('/csu', methods=['PUT'])
def update_csu():
    pass


@api.route('/<uid>', methods=['GET'])
@auth.login_required
def get_user_uid(uid):
    uid = user_verify.verify_uid(uid)
    user = user_org.get_user_by_uid(uid)
    if user:
        return jsonify(user), 200
    else:
        raise NotFound('user not found', 2000)

