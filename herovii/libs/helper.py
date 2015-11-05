__author__ = 'bliss'

from .enums import MobileRace
from enum import Enum


def get_url_no_param(request):
    full_path = str(request.full_path)
    q_index = full_path.find('?')
    full_path = full_path[0:q_index]

    return full_path


def android_ipad_iphone(http_user_agent):

    if 'iPhone' in http_user_agent:
        return MobileRace.iphone

    if 'iPad' in http_user_agent:
        return MobileRace.ipad

    if 'Android' in http_user_agent:
        return MobileRace.android

    return MobileRace.other

