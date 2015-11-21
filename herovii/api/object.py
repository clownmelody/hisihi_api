import json
from flask import request, jsonify
from werkzeug.exceptions import RequestEntityTooLarge
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import ParamException
from herovii.service.file import FilePiper

__author__ = 'bliss'

api = ApiBlueprint('object')


@api.route('', methods=['POST'])
def upload_object():
    try:
        files_list = request.files.lists()
    except RequestEntityTooLarge:
        raise ParamException(error='upload file length is too large',
                             error_code=4003, code=413)

    file_piper = FilePiper(files_list)
    files_urls = file_piper.upload_to_oss()
    return json.dumps(files_urls), 201


