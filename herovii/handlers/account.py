# __author__ = 'bliss'
#
# from flask import jsonify, request, g, json
# from flask.ext.httpauth import HTTPBasicAuth
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import SignatureExpired, BadSignature
# from flask import current_app
#
# from herovii.service import account
# from herovii.libs.error_code import AuthFailed, UnknownError, ParamException
# from herovii.libs.bpbase import ApiBlueprint
# from herovii.libs.httper import BMOB
# from herovii.validator.forms import RegisterByMobileForm, GetTokenForm
# from herovii.libs.helper import success_json
# from herovii.libs.scope import is_in_scope
# from herovii.libs.enums import AccountTypeEnum
#
# api = ApiBlueprint('account')
# auth = HTTPBasicAuth()
#
#
# @api.route('/token', methods=['POST'])
# def get_token():
#     """ 获取token接口
#     :POST:
#         {"uid": uid, "secret": secret, "type": type}
#     :argument:
#         uid 用户名称或者App的代号
#         secret 用户密码或者App的Secret
#         type 账号类型
#     :return:
#     """
#     # uid = g.uid
#     form = GetTokenForm.create_api_form()
#     valid = verify(form.uid.data, form.secret.data, form.type.data)
#     if not valid:
#         raise AuthFailed()
#     expiration = current_app.config['TOKEN_EXPIRES_IN']
#     token = generate_auth_token(form.uid.data, form.type.data, expiration)
#     return jsonify({'token': token.decode('ascii')}), 200
#
#
# def refresh_token():
#     pass
#
#
# @api.route('/reset-password', methods=['PUT'])
# def find_password():
#     """ 重置/找回密码
#         调用此接口需要先调用'/v1/sms/verify' 接口，以获得短信验证码
#     :PUT:
#         {"phone_number":'18699998888', "sms_code":'876876', "password":'password'}
#     :return:
#     """
#     bmob = BMOB()
#     form = RegisterByMobileForm.create_api_form()
#     mobile = form.phone_number.data
#     password = form.password.data
#     sms_code = form.sms_code.data
#     status, body = bmob.verify_sms_code(mobile, sms_code)
#     if status == 200:
#         account.reset_password_by_mobile(mobile, password)
#         return success_json(), 202
#     else:
#         j = json.loads(body)
#         raise UnknownError(j['error'], error_code=None)
#
#
# def verify(uid, secret, ac_type):
#     try:
#         if str.isnumeric(ac_type):
#             ac_type = int(ac_type)
#             ac_type = AccountTypeEnum(ac_type)
#         else:
#             ac_type = AccountTypeEnum[ac_type]
#     except ValueError:
#         raise ParamException(error='the type parameter is not in range')
#     promise = {AccountTypeEnum.App: account.verify_in_heroapi}
#     return promise.get(ac_type)(uid, secret)
#
#
# @auth.verify_password
# def verify_password(token, password):
#     if current_app.config['REMOVE_TOKEN_VERIFY']:
#         return True
#     uid = verify_auth_token(token)
#     if not uid:
#         return False
#     else:
#         g.uid = uid
#         return True
#
#
# @auth.error_handler
# def error_handler():
#     raise AuthFailed()
#
#
# def generate_auth_token(uid, ac_type, expiration=7200):
#         s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
#         return s.dumps({'uid': uid, 'ac_type': ac_type, 'scope': 'user'})
#
#
# def verify_auth_token(token):
#     s = Serializer(current_app.config['SECRET_KEY'])
#     try:
#         data = s.loads(token)
#     except SignatureExpired:
#         raise AuthFailed(error='token is expired', error_code=1003)
#         # return None # valid token, but expired
#     except BadSignature:
#         raise AuthFailed(error='token is invalid', error_code=1002)
#         # return None # invalid token
#
#     uid = data['uid']
#     scope = data['scope']
#     if not current_app.config['REMOVE_SCOPE_CONTROL']:
#         allow = is_in_scope(scope, request.endpoint)
#         if not allow:
#             raise AuthFailed(error='forbidden,not in scope', error_code=1004, code='403')
#     return uid
#
#
