from flask import request, redirect, jsonify
from flask import current_app, g
from werkzeug.exceptions import RequestEntityTooLarge
from herovii.libs.bpbase import ApiBlueprint
from herovii.api.token import auth
from herovii.libs.error_code import ParamException, FileUploadFailed
from herovii.libs.helper import allowed_uploaded_file_type, success_json
from herovii.libs.oss import OssAPI
from herovii.libs.util import get_timestamp_with_random, file_extension, year_month_day
from herovii.validator.forms import OnlineIDForm

__author__ = 'bliss'

api = ApiBlueprint('test')


@api.route('/get', methods=['GET'])
def bbb():
    p = request.args.get('name')
    return p, 200


@api.route('/')
def aaa():
    a = current_app.config['ALI_OSS_HOST']
    s = current_app.config['ALI_OSS_CDN_HOST']
    return 'ok', 200