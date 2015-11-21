from flask import request
from flask import current_app
from werkzeug.exceptions import RequestEntityTooLarge
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import ParamException, FileUploadFailed
from herovii.libs.helper import allowed_uploaded_file_type, success_json
from herovii.libs.oss import OssAPI
from herovii.libs.util import get_timestamp_with_random, file_extension, year_month_day

__author__ = 'bliss'

api = ApiBlueprint('file')


@api.route('/', methods=['POST'])
def upload_files():
    try:
        files_list = request.files.lists()
    except RequestEntityTooLarge:
        raise ParamException(error='upload file length is too large',
                             error_code=4003, code=413)

    file_urls_dict = {}
    for key, files in files_list:
        files_urls = []
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


