# -*- coding: utf-8 -*-
__author__ = 'bliss'

from werkzeug._compat import text_type
from flask import json
from .errors import APIException


class Successful(object):
    code = 201
    msg = 'ok'
    error_code = 0

    def __init__(self, uri, code=None, msg=None, error_code=None):
        self.uri = uri
        if code is not None:
            self.code = code
        if msg is not None:
            self.msg = msg
        if error_code is not None:
            self.error_code = error_code

    def get_json(self):
        return text_type(json.dumps(dict(
            msg=self.msg,
            code=self.error_code,
            request=self.uri
        )))


class ParamException(APIException):
    code = 400
    error = 'invalid_parameter'
    error_code = 1000

    # def __init__(self, error='invalid_parameter', code=400, error_code=1000, response=None):
    #     super().__init__(error, error_code, code, response)


class DataArgumentsException(APIException):
    code = 200
    error = 'data arguments logic exception'
    error_code = 5005


class JSONStyleError(APIException):
    code = 400
    error = ('the input json data is invalid,caution: '
             'the name of json data,should be'
             'in double quotation marks')
    error_code = 1006


class NotFound(APIException):
    code = 404
    error = 'the resource are not_found O__O...'
    error_code = 1001


class ServerError(APIException):
    code = 500
    error = 'sorry, we made a mistake O__O...'
    error_code = 1007


class UpdateDBError(APIException):
    code = 500
    error = 'sorry, we made a mistake O__O...'
    error_code = 6000


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    # WWW-Authenticat 响应头是为了支持Android解析401 状态码的响应
    headers = {
     'WWW-Authenticate': 'xBasic realm=""',
     'Content-Type': 'application/json'
    }
    error = 'authorization failed'


class IllegalOperation(APIException):
    code = 403
    error_code = 1008
    error = 'your operation is illegal'


class VolumeTooLarge(APIException):
    code = 413
    error_code = 5001
    error = 'Volume is too large'


class FileUploadFailed(APIException):
    code = 413
    error_code = 4001
    error = 'uploaded to oss failed'


class OrgNotFound(APIException):
    code = 404
    error_code = 5000
    error = 'org not found'


class StuClassNotFound(APIException):
    code = 404
    error_code = 5006
    error = 'class not found according to uid'


class UnknownError(APIException):
    code = 400
    error_code = 999
    error = 'sorry, there is a unknown error,suck!'


class CreateImGroupFailture(APIException):
    code = 200
    error_code = 7000
    error = 'create im group failture'


class UpdateImGroupFailture(APIException):
    code = 200
    error_code = 7001
    error = 'update im group name failture'


class DeleteImGroupFailture(APIException):
    code = 200
    error_code = 7002
    error = 'delete im group failture'


class ImGroupNotFound(APIException):
    code = 200
    error_code = 7003
    error = 'im group not found according to group_id'


class AddGroupMemberFailture(APIException):
    code = 200
    error_code = 7004
    error = 'add member to group failture'


class DeleteImGroupMemberFailture(APIException):
    code = 200
    error_code = 7005
    error = 'delete im group member failture'


class DirtyDataError(APIException):
    code = 200
    error_code = 1009
    error = 'some dirty data in the database'


class PushToClassFailture(APIException):
    code = 200
    error_code = 7007
    error = 'you have send message today'


class SendSysMessageFailture(APIException):
    code = 200
    error_code = 7008
    error = 'send sys message failture, not found target'


class CouponOutOfDateFailture(APIException):
    code = 200
    error_code = 8000
    error = 'the coupon is out of date'


class CouponHasObtainedFailture(APIException):
    code = 200
    error_code = 8001
    error = 'the coupon has been obtained'


class GiftHasObtainedFailture(APIException):
    code = 200
    error_code = 8002
    error = 'you have submitted the gift request'


class CreateOrderFailure(APIException):
    code = 200
    error_code = 10001
    error = 'create order failed'


class OrderNotFindFailure(APIException):
    code = 404
    error_code = 10002
    error = 'order not find'


class OrderAlreadyPayFailure(APIException):
    code = 200
    error_code = 11001
    error = 'order has been pay'


class UserRebateNotFindFailure(APIException):
    code = 404
    error_code = 10003
    error = 'user rebate not find'


class RebateExpiredFailure(APIException):
    code = 200
    error_code = 10004
    error = 'the rebate has expired'


class WeixinHasBindOrgFailure(APIException):
    code = 200
    error_code = 10005
    error = 'the weixin account has bind org'


class RebateIsDisabledFailure(APIException):
    code = 200
    error_code = 10006
    error = 'the rebate is disabled'