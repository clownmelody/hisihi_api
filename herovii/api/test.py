from flask import request, redirect, jsonify
from flask import current_app, g
from werkzeug.exceptions import RequestEntityTooLarge
from herovii.libs.bpbase import ApiBlueprint
from herovii.api.token import auth
from herovii.libs.error_code import ParamException, Successful, FileUploadFailed
from herovii.libs.helper import allowed_uploaded_file_type, success_json
from herovii.libs.oss import OssAPI
from herovii.libs.util import get_timestamp_with_random, file_extension, year_month_day
from herovii.models.org import OrgInfo

__author__ = 'bliss'

api = ApiBlueprint('test')


@api.route('/get', methods=['GET'])
def test_javascript_http():
    p = request.args.get('name')
    return p, 200


@api.route('/')
def nothing():
    id = 1
    a = OrgInfo.query.filter_by(id=id).first()
    s = a.id
    return jsonify(a), 200


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
    uid = g.user[0]
    return 'success', 200



