__author__ = 'bliss'

from enum import Enum


class MobileRaceEnum(Enum):
    """手机操作系统分类"""
    iphone = 1
    ipad = 2
    android = 3
    other = 4


class DownloadChannelEnum(Enum):
    """
    表示官网App包的下载途径
    online = 1 ,表示通过活动途径下载
    """
    online = 1


class AccountTypeEnum(Enum):
    """账号类型，主要用于找到相应的数据库表"""
    app = 100
    user_csu_mobile = 200
    user_csu_wechat = 201
    user_csu_weibo = 202
    user_csu_qq = 203
    use_csu_social = 230
    user_org_mobile = 300


class TagType(Enum):
    """所有文本标签类共用一个表，用类型区别"""
    # 机构类型类
    org_type = 100

    # 机构优势类
    org_advantage = 101


class UserCSUIdentity(Enum):
    """用户身份类型"""
    normal = 1
    designer = 5
    teacher = 6
    server_admin = 7
    super = 8


class OrgAuditStatus(Enum):
    """机构审核状态"""
    wait = 0
    in_progress = 1
    done = 2
    success = 3
    reject = 4


class OrgPicType(Enum):
    """机构图片类型"""
    student = 1
    environment = 2

