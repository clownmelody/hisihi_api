__author__ = 'bliss'

from werkzeug._compat import text_type
from flask import json, request
from .errors import APIException
from herovii.libs.helper import get_url_no_param


class Succesful(object):
    code = 201
    msg = 'ok'
    error_code = 0

    def __init__(self, code, msg, error_code):
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
            request=request.method+'  ' + get_url_no_param()
        )))


class ParamException(APIException):
    code = 400
    error = 'invalid_parameter'
    error_code = 1000

    def __init__(self, error='invalid_parameter', code=400, error_code=1000, response=None):
        super().__init__(error, error_code, code, response)


class NotFound(APIException):
    code = 404
    error = 'the resource are not_found'
    error_code = 1001


class AuthFaild(APIException):
    code = 401
    error_code = 1002
    error = 'Authorization is required'


class UnknownError(APIException):
    code = 500
    error_code = 999
    error = 'sorry, there is a unknown error,suck!'

