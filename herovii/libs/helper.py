__author__ = 'bliss'

from flask import request
from .enums import MobileRaceEnum
from .error_code import Successful


def get_url_no_param():
    full_path = str(request.full_path)
    q_index = full_path.find('?')
    full_path = full_path[0:q_index]

    return full_path


def android_ipad_iphone(http_user_agent):

    if 'iPhone' in http_user_agent:
        return MobileRaceEnum.iphone

    if 'iPad' in http_user_agent:
        return MobileRaceEnum.ipad

    if 'Android' in http_user_agent:
        return MobileRaceEnum.android

    return MobileRaceEnum.other


def success_json(code=None, msg=None, error_code=None):
    url = request.method+'  ' + get_url_no_param()
    return Successful(url, code, msg, error_code).get_json()

