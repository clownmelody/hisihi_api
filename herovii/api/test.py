from flask import request, redirect
from flask import current_app, g
from flask.helpers import url_for
from flask.json import jsonify
from werkzeug.exceptions import RequestEntityTooLarge
from herovii.libs.bpbase import ApiBlueprint
from herovii.api.token import auth
from herovii.libs.error_code import ParamException, FileUploadFailed
from herovii.libs.helper import allowed_uploaded_file_type, success_json
from herovii.libs.oss import OssAPI
from herovii.libs.util import get_timestamp_with_random, file_extension, year_month_day
from herovii.cache import cache

__author__ = 'bliss'

api = ApiBlueprint('test')


@api.route('/get', methods=['GET'])
def test_javascript_http():
    p = request.args.get('name')
    return p, 200


# @api.route('/')
# def nothing():
#     a = current_app.config['ALI_OSS_HOST']
#     s = current_app.config['ALI_OSS_CDN_HOST']
#     return 'ok', 200

@api.route('/redis', methods=['GET'])
@cache.cached(timeout=60, key_prefix='test')
def test_redis_cache():
    return jsonify({'name': 'leilei'}), 200


@api.route('', methods=['POST'])
def nothing_1():
    return 'ok', 201


@api.route('/client-ip', methods=['GET'])
@cache.cached(timeout=120, key_prefix='client-ip')
def test_client_ip():
    r = request.remote_addr
    return r, 200


@api.route('/2.6/client-ip', methods=['GET'])
@cache.cached(timeout=120, key_prefix='client-ip2.6')
def test_client_ip_v26():
    r = request.remote_addr
    return r, 200


@api.route('/dev/<int:uid>')
def test_new_dev(uid):
    s = url_for('test_new_dev', uid=3)
    a = 1/0
    return 'dev is ok', 200


@api.route('/redirect')
def test_redirect():
    return redirect('http://sina.com')


@api.route('/oss', methods=['POST'])
def test_oss_put_object():
    try:
        files_list = request.files.lists()
    except RequestEntityTooLarge:
        raise ParamException(error='upload file length is too large',
                             error_code=4003, code=413)

    for key, files in files_list:
        for file in files:
            allowed = allowed_uploaded_file_type(file.filename)
            if not allowed:
                raise ParamException(error='extension of the file is forbidden for upload',
                                     error_code=4002, code=403)
            random_name = get_timestamp_with_random() + '.' + file_extension(file.filename)
            f = file.stream
            oss = OssAPI(access_id=current_app.config['ALI_OSS_ID'], is_security=True,
                         secret_access_key=current_app.config['ALI_OSS_SECRET'])
            oss_url = year_month_day() + '/' + random_name

            try:
                res = oss.put_object_from_fp(current_app.config['ALI_OSS_ORG_BUCKET_NAME'], oss_url, f)
                if res.code == 200:
                    continue
                else:
                    raise FileUploadFailed()
            except:
                raise FileUploadFailed()
    return success_json()


@api.route('/error-log')
def test_error_log():
    i = 2/0
    return i, 200


@api.route('/auth')
@auth.login_required
def test_auth():
    uid = g.user[0]
    return 'success', 200


@api.route('/test')
def test_test():
    str1 = request.values.get('echostr')
    return str1


@api.route('/user/agent')
def test_user_agent():
    str1 = request.headers.get('User-Agent')
    return jsonify({'info': str1}), 200