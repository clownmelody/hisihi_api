import sys
from flask import request
from flask import current_app
from werkzeug.exceptions import RequestEntityTooLarge
from herovii.libs.error_code import ParamException, FileUploadFailed
from herovii.libs.helper import allowed_uploaded_file_type, success_json, get_oss_file_url
from herovii.libs.oss import OssAPI
from herovii.libs.util import get_timestamp_with_random, file_extension, year_month_day

__author__ = 'bliss'


class FilePiper(object):

    def __init__(self, files_list):
        self.files_list = files_list

    def upload_to_oss(self):
        """上传一组文件到OSS（多Key）"""
        file_urls_dict = {}

        for key, files in self.files_list:
            file_urls = FilePiper.upload_batch_to_oss(files)
            file_urls_dict.update({key: file_urls})
        return file_urls_dict

    @staticmethod
    def upload_batch_to_oss(files):
        """上传一组文件到OSS（单Key）"""
        file_urls = []
        for file in files:
                url = FilePiper.upload_one_to_oss(file)
                file_urls.append(url)
        return file_urls

    @staticmethod
    def upload_bytes_to_oss(f):
        oss = OssAPI(access_id=current_app.config['ALI_OSS_ID'], is_security=True,
                     secret_access_key=current_app.config['ALI_OSS_SECRET'])
        object_url = get_oss_file_url('png')
        try:
            res = oss.put_object_from_fp(current_app.config['ALI_OSS_ORG_BUCKET_NAME'], object_url, f)
            if res.code == 200:
                return FilePiper.get_full_oss_url(object_url, True)
            else:
                raise FileUploadFailed()
        except:
            raise FileUploadFailed()
        # finally:)
        #     res.close(

    @staticmethod
    def upload_text_to_oss(f, extension, directory, content_type):
        oss = OssAPI(access_id=current_app.config['ALI_OSS_ID'], is_security=True,
                     secret_access_key=current_app.config['ALI_OSS_SECRET'])
        object_url = directory + '/' + get_oss_file_url(extension)
        try:
            res = oss.put_object_from_string(current_app.config['ALI_OSS_ORG_BUCKET_NAME'], object_url, f,
                                             content_type)
            if res.code == 200:
                return FilePiper.get_full_oss_url(object_url, True)
            else:
                raise FileUploadFailed()
        except:
            info = sys.exc_info()
            raise FileUploadFailed()

    @staticmethod
    def upload_one_to_oss(file):
        """上传单一文件到OSS"""
        allowed = allowed_uploaded_file_type(file.filename)
        if not allowed:
            raise ParamException(error='extension of the file is forbidden for upload',
                                 error_code=4002, code=403)
        # random_name = get_timestamp_with_random() + '.' + file_extension(file.filename)
        f = file.stream
        oss = OssAPI(access_id=current_app.config['ALI_OSS_ID'], is_security=True,
                     secret_access_key=current_app.config['ALI_OSS_SECRET'])
        extension = file_extension(file.filename)
        object_url = get_oss_file_url(extension)

        try:
            res = oss.put_object_from_fp(current_app.config['ALI_OSS_ORG_BUCKET_NAME'], object_url, f)
            if res.code == 200:
                return FilePiper.get_full_oss_url(object_url, True)
            else:
                raise FileUploadFailed()
        except:
            raise FileUploadFailed()

    @staticmethod
    def get_full_oss_url(object_url, cdn=False):
        if cdn:
            host = current_app.config['ALI_OSS_CDN_HOST']
            full_oss_url = 'http://' + host + '/' + object_url
        else:
            host = current_app.config['ALI_OSS_HOST']
            bucket = current_app.config['ALI_OSS_ORG_BUCKET_NAME']
            full_oss_url = 'http://'+bucket + '.' + host + '/' + object_url

        return full_oss_url










