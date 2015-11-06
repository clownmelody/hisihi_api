__author__ = 'bliss'

from enum import Enum


class MobileRace(Enum):
    iphone = 1
    ipad = 2
    android = 3
    other = 4


class DownloadChannel(Enum):
    """
    表示官网App包的下载途径
    online = 1 ,表示通过活动途径下载
    """
    online = 1

