__author__ = 'bliss'

from flask import jsonify, request, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app

from herovii.service import account
from herovii.libs.error_code import AuthFailed, ParamException, JSONStyleError
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.validator.forms import GetTokenForm
from herovii.libs.scope import is_in_scope
from herovii.libs.enums import AccountTypeEnum

api = ApiBlueprint('token')


@api.route('', methods=['POST'])
def get_token():
    """ 获取token接口
    :POST:
        {"uid": uid, "secret": secret, "type": type}
    :argument:
        uid 用户名称或者App的代号
        secret 用户密码或者App的Secret
        type 账号类型
    :return:
    """
    # uid = g.uid
    form = GetTokenForm.create_api_form()
    scope = verify(form.uid.data, form.secret.data, form.type.data)
    if scope is None:
        raise AuthFailed(error='id or password is incorrect', error_code=1005)
    expiration = current_app.config['TOKEN_EXPIRES_IN']
    token = generate_auth_token(form.uid.data, form.type.data, scope, expiration)
    return jsonify({'token': token.decode('ascii')}), 201


@api.route('/info', methods=['POST'])
def get_token_info():
    json = request.get_json(force=True, silent=True)
    if not json:
        raise JSONStyleError()
    else:
        s = Serializer(current_app.config['SECRET_KEY'])
        token = json['token']
        try:
            data = s .loads(token, return_header=True)
        except SignatureExpired:
            raise AuthFailed(error='token is expired', error_code=1003)
        except BadSignature:
            raise AuthFailed(error='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],
        'expire_in': data[1]['exp']
    }
    return jsonify(r), 200


def refresh_token():
    pass


def verify(uid, secret, ac_type):
    try:
        if isinstance(ac_type, int) or str.isnumeric(ac_type):
            ac_type = int(ac_type)
            ac_type = AccountTypeEnum(ac_type)
        else:
            ac_type = AccountTypeEnum[ac_type]
    except ValueError:
        raise ParamException(error='the type parameter is not in range')
    promise = {AccountTypeEnum.app: account.verify_in_heroapi}
    return promise.get(ac_type)(uid, secret)


@auth.verify_password
def verify_password(token, password):
    # Todo 开发时取消验证
    if current_app.config['REMOVE_TOKEN_VERIFY']:
        return True
    uid = verify_auth_token(token)
    if not uid:
        return False
    else:
        g.uid = uid
        return True


@auth.error_handler
def error_handler():
    raise AuthFailed()


def generate_auth_token(uid, ac_type, scope, expiration=7200):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'uid': uid, 'ac_type': ac_type, 'scope': scope})


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        # data = s.loads(token)
        data = s.loads(token)
    except SignatureExpired:
        raise AuthFailed(error='token is expired', error_code=1003)
        # return None # valid token, but expired
    except BadSignature:
        raise AuthFailed(error='token is invalid', error_code=1002)
        # return None # invalid token

    uid = data['uid']
    scope = data['scope']
    if not current_app.config['REMOVE_SCOPE_CONTROL']:
        allow = is_in_scope(scope, request.endpoint)
        if not allow:
            raise AuthFailed(error='forbidden,not in scope', error_code=1004, code='403')
    return uid


