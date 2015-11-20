import os, sys
import stat

__author__ = 'bliss'

from flask import request, redirect

from herovii.libs.bpbase import ApiBlueprint
from herovii.api.token import auth

api = ApiBlueprint('test')


@api.route('/get', methods=['GET'])
def test_javascript_http():
    p = request.args.get('name')
    return p, 200


@api.route('/client-ip', methods=['GET'])
def test_client_ip():
    r = request.remote_addr
    return r, 200


@api.route('/dev')
def test_new_dev():
    a = 1/0
    return 'dev is ok', 200


@api.route('/redirect')
def test_redirect():
    return redirect('http://sina.com')


@api.route('/oss', methods=['POST'])
def test_oss_put_object():
    # file_object = open('E:/test/t.txt', 'w')
    # file_object.write('ddddddddddd')
    # file_object.close( )
    # # os.chmod("E:/test", stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    r =request
    file = request.files['file']
    print(os.path.join('E:/test', file.filename))
    if file:
        file.save(os.path.join('E:/test', file.filename))
    return 'ok', 200


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



