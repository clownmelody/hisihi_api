__author__ = 'bliss'

from herovii.libs.error_code import AuthFailed


class ScopeBase(object):
    allow_module = []
    forbidden = []
    allow_api = []

    def __add__(self, other):
        """重载Scope类的 + 操作
        用户权限通常来说总是大于应用程序基础权限,
        所以我们需要将用户权限和应用程序基础权限叠加
        """
        # 合并两个列表
        self.allow_module = self.allow_module + other.allow_module
        # 去重
        self.allow_module = list(set(self.allow_module))

        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))

        # forbidden 需要进行相减操作。
        self.forbidden_api = list(set(self.forbidden_api) - set(other.forbidden_api))


class Online0001Scope(ScopeBase):
    """"基础活动权限，仅有统计数据的接口权限"""
    allow_module = ['v1.online', 'v1.pk', 'v1.test']
    forbidden = ['v1.test+test_auth']


class UserCSUScope(ScopeBase):
    """消费用户权限域"""
    allow_api = ['v1.mall+redirect_to_duiba', 'v1.test+test_auth']
    allow_module = ['v1.user']
    forbidden = ['v1.user+change_identity']


class OrgBaseScope(ScopeBase):
    """第一方Org应用程序的权限域"""
    allow_api = ['v1.sms+send_sms_code', 'v1.tag+get_tags']
    allow_module =['v1.org']


class OrgAdminScope(ScopeBase):
    """Org管理员用户应用权限"""
    allow_api = ['v1.file+upload_object', 'v1.test+test_auth', 'v1.user+change_identity'] + OrgBaseScope.allow_api
    allow_module = ['v1.org'] + OrgBaseScope.allow_module


def is_in_scope(scope, api_endpoint):
    try:
        scope_class = globals()[scope+'Scope']
    except KeyError:
        raise AuthFailed(error='forbidden,not in scope', error_code=1004, code='403')
    index = str.find(api_endpoint, '+')
    module = api_endpoint[:index]

    if api_endpoint in scope_class.allow_api:
        return True
    if module in scope_class.allow_module and api_endpoint not in scope_class.forbidden \
            and module not in scope_class.forbidden:
        return True
    return False
