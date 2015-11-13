__author__ = 'bliss'

from herovii.libs.error_code import AuthFailed


class Online0001Scope(object):
    """"基础活动权限，仅有统计数据的接口权限"""
    allow_module = ['v1.online', 'v1.pk', 'v1.test']
    forbidden_api = ['v1.test+test_auth']
    allow_api = []

    # @staticmethod
    # def is_in_scope(api_endpoint):
    #     index = str.find(api_endpoint, '+')
    #     prefix = api_endpoint[:index]
    #
    #     if api_endpoint in Online0001Scope.allow_api:
    #         return True
    #     if prefix in Online0001Scope.allow_module and prefix not in Online0001Scope.forbidden_api:
    #         return True
    #     return False


class UserCSUScope(object):
    """消费用户权限域"""
    allow_module = []
    forbidden_api = []
    allow_api = ['v1.mall+redirect_to_duiba']


def is_in_scope(scope, api_endpoint):
    try:
        scope_class = globals()[scope+'Scope']
    except KeyError:
        raise AuthFailed(error='forbidden,not in scope', error_code=1004, code='403')
    index = str.find(api_endpoint, '+')
    prefix = api_endpoint[:index]

    if api_endpoint in scope_class.allow_api:
        return True
    if prefix in scope_class.allow_module and prefix not in scope_class.forbidden_api:
        return True
    return False
