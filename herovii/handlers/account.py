__author__ = 'bliss'

from flask import jsonify, request, g, json
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app

from herovii.service import account
from herovii.libs.error_code import AuthFaild, Successful, UnknownError
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.httper import BMOB
from herovii.validator.forms import RegisterByMobileForm
from herovii.libs.helper import success_json

api = ApiBlueprint('account')
auth = HTTPBasicAuth()


@api.route('')
@auth.login_required
def get_auth_token():
    uid = g.id
    token = generate_auth_token(uid)
    return jsonify({'token': token.decode('ascii')}), 200


@api.route('/reset-password', methods=['PUT'])
def find_password():
    """ 重置/找回密码
        调用此接口需要先调用'/v1/sms/verify' 接口，以获得短信验证码
    :PUT:
        {'phone_number':'18699998888', 'sms_code':'876876', 'password':'password'}
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


@auth.verify_password
def verify_password(username_or_token, password):
    # Todo 开发时取消验证
    return True
    r = request
    print(r.headers)
    uid = verify_auth_token(username_or_token)
    if not uid:
        uid = account.verify_by_phonenumber(username_or_token, password)
        if not uid:
            return False
        else:
            g.uid = uid
            return True
    else:
        g.uid = uid
        return True


@auth.error_handler
def error_handler():
    raise AuthFaild()


def generate_auth_token(uid, expiration=2000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': uid})


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    uid = data['id']
    return uid


