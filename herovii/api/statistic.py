__author__ = 'bliss'

from flask import json, jsonify, request
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.helper import android_ipad_iphone, success_json
from herovii.libs.error_code import Succesful, UnknownError
from herovii.service.statistic import downloads_plus

api = ApiBlueprint('statistic')


@api.route('/download+1', methods=['PUT'])
def downloads_plus_1():
    """ 下载数+1
    :PUT:
        sample: {"oid":"3"}
    :Arg:
        sample: ?channel = 1
    :return:
    """
    j = request.get_json()
    channel = request.args.get('channel')
    r = request.remote_addr
    head_agent = request.user_agent.string
    mobile_race = android_ipad_iphone(head_agent)
    count = downloads_plus(channel, oid=j['oid'], mobile_race=mobile_race)
    if count >= 1:
        return success_json(), 202
    else:
        raise UnknownError()

def pv_plus_1():
    pass


def finished_plus_1():
    pass


def uv_plus_1():
    pass