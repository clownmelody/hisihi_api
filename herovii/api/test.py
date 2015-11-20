from flask import request, redirect
from flask import current_app
from herovii.libs.bpbase import ApiBlueprint
from herovii.api.token import auth
from herovii.libs.oss import OssAPI
from herovii.libs.util import get_timestamp_with_random, file_extension, year_month_day

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
    uploaded_files = request.files.getlist('files')
    for file in uploaded_files:
        random_name = get_timestamp_with_random() + '.' + file_extension(file.filename)
        f = file.stream
        oss = OssAPI(access_id=current_app.config['ALI_OSS_ID'], is_security=True,
                     secret_access_key=current_app.config['ALI_OSS_SECRET'])
        oss_url = year_month_day() + '/' + random_name
        oss.put_object_from_fp(current_app.config['ALI_OSS_ORG_BUCKET_NAME'], oss_url, f)
    # print(f.getvalue())
    # fw = open('D:/321.jpg', 'wb')
    # fw.write(file.getvalue())
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



