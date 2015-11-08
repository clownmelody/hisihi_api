__author__ = 'bliss'

from flask import request
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.helper import android_ipad_iphone, success_json
from herovii.libs.error_code import UnknownError
from herovii.service.pk import downloads_plus
from herovii.validator.forms import DownloadPlus1Form
from herovii.libs.bpbase import auth

api = ApiBlueprint('pk')


@api.route('/download+1', methods=['PUT'])
@auth.login_required
def downloads_plus_1():
    """ 下载数+1, channel表示通过哪一种方式新增的下载量
    channel = online or 1 表示通过活动新增的下载量，此时PUT的Data中需要包含'oid'
    参数，表示活动号
    :PUT:
        sample: {"oid":"3", "channel":"online"}
    :Arg:
        sample: ?channel = 1 or channel = online
    :return:
    """
    form = DownloadPlus1Form().create_api_form()

    head_agent = request.user_agent.string
    mobile_race = android_ipad_iphone(head_agent)
    count = downloads_plus(form.channel.data, oid=form.oid.data, mobile_race=mobile_race)
    if count >= 1:
        return success_json(), 202
    else:
        raise UnknownError()

