__author__ = 'bliss'

from urllib import request


class SMS(object):
    BMOB_SMS_CODE_API = 'https://api.bmob.cn/1/requestSmsCode'

    def send_verify_code_by_bmob(self, app_id, key_id, mobile_number):
        request(SMS.BMOB_SMS_CODE_API)
        pass
