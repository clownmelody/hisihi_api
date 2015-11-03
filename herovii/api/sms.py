__author__ = 'bliss'

# just for web application. web application need server to help receive the verify sms
# for mobile, it  doesn't need the server to receive sms.

from flask import json
from herovii.api.base import ApiBlueprint
from herovii.libs.httper import BMOB
from herovii.validator.forms import PhoneNumberForm
from herovii.libs.error_code import Succesful, UnknownError

api = ApiBlueprint('sms')


@api.route('/verify', methods=['POST'])
def send_verify_sms():
    """ 发送验证码短信
    发送一条验证码短信，默认使用bmob服务发送
    :return:
        返回操作成功信息
    """
    bmob = BMOB()
    form = PhoneNumberForm.create_api_form()
    phone_number = form.phone_number.data
    status, body = bmob.send_verify_sms(phone_number)
    if status == 200:
        ok = Succesful()
        return ok.get_json(), 201
    else:
        j = json.loads(body)
        raise UnknownError(j['error'], error_code=None)


@api.route('/ad', methods=['POST'])
def send_ad_sms():
    pass