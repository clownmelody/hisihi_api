__author__ = 'bliss'

from enum import Enum


class MobileRaceEnum(Enum):
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
    App = 1

