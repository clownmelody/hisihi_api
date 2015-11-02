__author__ = 'bliss'

# just for web application. web application need server to help receive the verify sms
# for mobile, it  doesn't need the server to receive sms.

from herovii.api.base import ApiBlueprint

api = ApiBlueprint('sms')


@api.route('/verify', methods=['POST'])
def send_verify_sms():
    """ 发送验证码短信
    发送一条验证码短信，默认使用bmob服务发送
    :return:
        返回操作成功信息
    """
    bmob_app_id = '8bee8ad5acaaa664f2f644c9e3a37c2e'
    bmob_api_key = '62060704177b04ee83d1bbc3778d5051'
    pass


@api.route('/ad', methods=['POST'])
def send_ad_sms():
    pass