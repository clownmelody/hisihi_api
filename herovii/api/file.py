import json
from flask import request, jsonify
from werkzeug.exceptions import RequestEntityTooLarge
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import ParamException
from herovii.libs.helper import make_a_qrcode
from herovii.service.file import FilePiper

__author__ = 'bliss'

api = ApiBlueprint('file')


@api.route('', methods=['POST'])
@auth.login_required
def upload_object():
    try:
        files_list = request.files.lists()
    except RequestEntityTooLarge:
        raise ParamException(error='upload file length is too large',
                             error_code=4003, code=413)

    file_piper = FilePiper(files_list)
    files_urls = file_piper.upload_to_oss()
    return json.dumps(files_urls), 201


@api.route('/qrcode', methods=['POST'])
# @auth.login_required
def create_a_qrcode():
    json_url = request.get_json(force=True)
    url = json_url['url']
    f = make_a_qrcode(url)
    oss_url = FilePiper.upload_bytes_to_oss(f)
    data = {
        'qrcode_url': oss_url
    }
    return jsonify(data), 201