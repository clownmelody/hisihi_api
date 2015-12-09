
# just for web application. web application need server to help receive the verify sms
# for mobile, it  doesn't need the server to receive sms.

from flask import json
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.httper import BMOB
from herovii.libs.bpbase import auth
from herovii.validator.forms import PhoneNumberForm
from herovii.libs.error_code import UnknownError
from herovii.libs.helper import success_json

__author__ = 'bliss'


api = ApiBlueprint('sms')


@api.route('/verify', methods=['POST'])
@auth.login_required
def send_sms_code():
    """ 发送验证码短信
    发送一条验证码短信，默认使用bmob服务发送
    :POST:
    {'phone_number':'1869999xxxx'}
    :return:
        返回操作是否成功相关信息
    """
    bmob = BMOB()
    form = PhoneNumberForm.create_api_form()
    phone_number = form.data.mobile
    status, body = bmob.send_sms_code(phone_number)
    if status == 200:
        return success_json(), 201
    else:
        j = json.loads(body)
        raise UnknownError(j['error'], error_code=None)


@api.route('/ad', methods=['POST'])
def send_ad_sms():
    pass