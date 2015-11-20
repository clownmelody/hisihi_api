from flask import request, redirect

from herovii.libs.bpbase import ApiBlueprint
from herovii.api.token import auth
from herovii.libs.oss import OssAPI

__author__ = 'bliss'

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
    # file = request.files['file']
    file = request.files.to_dict()
    s = file.itms()
    f = file.stream
    # print(f.getvalue())
    # fw = open('D:/321.jpg', 'wb')
    # fw.write(file.getvalue())
    oss = OssAPI(access_id='3uFZDrxg6fGKZq8P', is_security=True,
                 secret_access_key='LxsXIcp7ghkyqABJYIHYjmcsku1VOS')
    oss.put_object_from_fp('hisihi-avator', 'xxx.jpg', f)

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



