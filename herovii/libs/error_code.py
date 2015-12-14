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
    error_code = 2001


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
    error_code = 1009


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


class UnknownError(APIException):
    code = 400
    error_code = 999
    error = 'sorry, there is a unknown error,suck!'

