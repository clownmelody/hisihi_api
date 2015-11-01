__author__ = 'bliss'

from .errors import APIException


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
