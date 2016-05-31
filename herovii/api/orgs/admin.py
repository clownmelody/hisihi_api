from flask import jsonify,  json
from herovii import db
from herovii.api.token import verify_user
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import  UnknownError, AuthFailed
from herovii.libs.httper import BMOB
from herovii.libs.helper import success_json
from herovii.models.org.org_admin_bind_weixin import OrgAdminBindWeixin
from herovii.service import account
from herovii.service.org import get_org_info_by_admin_id
from herovii.validator.forms import RegisterByMobileForm, VerifyOrgAdminForm, \
    AdminBindWeixinForm, VerifyCouponCodeForm
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
    mobile = form.mobile.data
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


@api.route('/verify/org/admin', methods=['POST'])
def verify_org_admin():
    form = VerifyOrgAdminForm.create_api_form()
    uid_scope = verify_user(form.account.data, form.secret.data, 300)
    if uid_scope is None:
        raise AuthFailed(error='id or password is incorrect', error_code=1005)
    org = get_org_info_by_admin_id(uid_scope[0])
    data = {
        'admin_id': uid_scope[0],
        'org': org
    }
    return jsonify(data), 200


@api.route('/admin/bind/weixin', methods=['POST'])
def admin_bind_weixin():
    form = AdminBindWeixinForm.create_api_form()
    org_admin_bind_weixin = OrgAdminBindWeixin()
    for key, value in form.body_data.items():
        setattr(org_admin_bind_weixin, key, value)
    with db.auto_commit():
        db.session.add(org_admin_bind_weixin)
    return jsonify(org_admin_bind_weixin), 201


@api.route('/admin/verify/coupon/code', methods=['POST'])
def verify_coupon_code():
    form = VerifyCouponCodeForm.create_api_form()
    org_admin_bind_weixin = OrgAdminBindWeixin()
    for key, value in form.body_data.items():
        setattr(org_admin_bind_weixin, key, value)
    with db.auto_commit():
        db.session.add(org_admin_bind_weixin)
    return jsonify(org_admin_bind_weixin), 201
