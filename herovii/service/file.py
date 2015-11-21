from flask import request
from flask import current_app
from werkzeug.exceptions import RequestEntityTooLarge
from herovii.libs.error_code import ParamException, FileUploadFailed
from herovii.libs.helper import allowed_uploaded_file_type, success_json
from herovii.libs.oss import OssAPI
from herovii.libs.util import get_timestamp_with_random, file_extension, year_month_day

__author__ = 'bliss'


class FilePiper(object):

    def __init__(self, files_list):
        self.files_list = files_list
        pass

    def upload_to_oss(self):
        file_urls_dict = {}

        for key, files in self.files_list:
            file_urls = []

            for file in files:
                url = FilePiper.upload_one_to_oss(file)
                file_urls.append(url)

            file_urls_dict.update({key: file_urls})
        return success_json()

    @staticmethod
    def upload_one_to_oss(file):
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
                return oss_url
            else:
                raise FileUploadFailed()
        except:
            raise FileUploadFailed()