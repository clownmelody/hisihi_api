__author__ = 'bliss'

from herovii.libs.enums import MobileRace
from herovii.models.onlines.statistic import Statistic
from herovii.models.base import db
from herovii.libs.enums import DownloadChannel
from herovii.libs.error_code import ParamException


def downloads_plus_by_online(**kwargs):
    oid = kwargs['oid']
    mobile_race = kwargs['mobile_race']
    params = {'f_online_id': oid}

    sqls = {
        MobileRace.android: {Statistic.android_downloads: Statistic.android_downloads+1},
        MobileRace.other: {Statistic.other_downloads: Statistic.other_downloads+1},
        MobileRace.ipad: {Statistic.ipad_downloads: Statistic.ipad_downloads+1},
        MobileRace.iphone: {Statistic.iphone_downloads: Statistic.iphone_downloads+1},
    }
    sql = sqls.get(mobile_race)

    with db.auto_commit():
        count = Statistic.query.filter_by(**params)\
            .update(sql)
    return count


def downloads_plus(channel, **kwargs):
    channels = {
        DownloadChannel.online: downloads_plus_by_online
    }
    if str.isnumeric(channel):
        channel = int(channel)
        try:
            key = DownloadChannel(channel)
        except ValueError:
            raise ParamException(error='the channel parameter is invalid')
    else:
        try:
            key = DownloadChannel(channel)
        except ValueError:
            raise ParamException(error='the channel parameter is invalid')

    return channels.get(key)(**kwargs)

