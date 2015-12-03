from flask import jsonify,  json
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import  UnknownError
from herovii.libs.httper import BMOB
from herovii.libs.helper import success_json
from herovii.service import account
from herovii.validator.forms import RegisterByMobileForm
from herovii.service.user_org import register_by_mobile

api = ApiBlueprint('org')


@api.route('/admin', methods=['POST'])
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


@api.route('/admin/password', methods=['PUT'])
def find_admin_password():
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


@api.route('/admin/<int:id>', methods=['GET'])
def get_org_admin(id):
    pass


@api.route('/admin/<int:id>', methods=['PUT'])
def update_org_admin(id):
    pass
