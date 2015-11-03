__author__ = 'bliss'

# just for web application. web application need server to help receive the verify sms
# for mobile, it  doesn't need the server to receive sms.

from herovii.api.base import ApiBlueprint
from herovii.libs.httper import BMOB
from herovii.validator.forms import PhoneNumberForm

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
    bmob.send_verify_sms(phone_number)


@api.route('/ad', methods=['POST'])
def send_ad_sms():
    pass