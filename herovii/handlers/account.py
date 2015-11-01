__author__ = 'bliss'

from flask import Blueprint, jsonify, request, g
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app

from herovii.service import account
from herovii.libs.error_code import AuthFaild

bp = Blueprint('account', __name__)
auth = HTTPBasicAuth()


@bp.route('/get-token')
@auth.login_required
def get_auth_token():
    uid = g.uid
    token = generate_auth_token(uid)
    return jsonify({ 'token': token.decode('ascii') })


@auth.verify_password
def verify_password(username_or_token, password):
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