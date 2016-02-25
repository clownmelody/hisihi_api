# -*- coding: utf-8 -*-
__author__ = 'bliss'

import traceback
from herovii.libs.error_code import ParamException


def verify_uid(uid):
    # 如果uid不是正整数
    error = 'the parameter uid must be an postive interger'
    try:
        uid = int(uid)
    except Exception:
        raise ParamException(error=error)

    if uid <= 0:
        raise ParamException(error=error)
    else:
        return uid
