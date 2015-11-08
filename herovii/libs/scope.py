__author__ = 'bliss'

from herovii.libs.error_code import AuthFailed


class OnlineScope(object):
    allow_module = ['v1.online', 'v1.pk', 'v1.test']
    forbidden_api = ['v1.test+test_auth']
    allow_api = []

    @staticmethod
    def is_in_scope(api_endpoint):
        index = str.find(api_endpoint, '+')
        prefix = api_endpoint[:index]

        if api_endpoint in OnlineScope.allow_api:
            return True
        if prefix in OnlineScope.allow_module and prefix not in OnlineScope.forbidden_api:
            return True
        return False


def is_in_scope(scope, api_endpoint):
    try:
        scope_class = globals()[scope+'Scope']
    except KeyError:
        raise AuthFailed(error='forbidden,not in scope', error_code=1004, code='403')

    in_scope = scope_class.is_in_scope(api_endpoint)
    return in_scope
