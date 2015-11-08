__author__ = 'bliss'

from flask import request, jsonify
from herovii.libs.bpbase import ApiBlueprint
from herovii.models.user_org import UserOrg
from herovii.models.base import db
from herovii.api.token import auth

api = ApiBlueprint('test')


@api.route('/get', methods=['GET'])
def test_javascript_http():
    return 'hello', 200


@api.route('/client-ip', methods=['GET'])
def test_client_ip():
    r = request.remote_addr
    return r, 200


@api.route('/download+1', methods=['PUT'])
def downloads_plus_1():
    pass


@api.route('/error-log')
def test_error_log():
    i = 2/0
    return i, 200


@api.route('/auth')
@auth.login_required
def test_auth():
    return 'success', 200


@api.route('/test', methods=['GET'])
def test():
    # pass
    user = UserOrg()
    user.password = '19851118'
    user.mobile = "18607131949"
    with db.auto_commit():
        db.session.add(user)
    return jsonify(user), 201

