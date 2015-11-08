__author__ = 'bliss'

from herovii.libs.enums import MobileRaceEnum
from herovii.models.onlines.statistic import Statistic
from herovii.models.base import db
from herovii.libs.enums import DownloadChannelEnum
from herovii.libs.error_code import ParamException


def downloads_plus_by_online(**kwargs):
    oid = kwargs['oid']
    mobile_race = kwargs['mobile_race']
    params = {'f_online_id': oid}

    sqls = {
        MobileRaceEnum.android: {Statistic.android_downloads: Statistic.android_downloads+1},
        MobileRaceEnum.other: {Statistic.other_downloads: Statistic.other_downloads+1},
        MobileRaceEnum.ipad: {Statistic.ipad_downloads: Statistic.ipad_downloads+1},
        MobileRaceEnum.iphone: {Statistic.iphone_downloads: Statistic.iphone_downloads+1},
    }
    sql = sqls.get(mobile_race)

    with db.auto_commit():
        count = Statistic.query.filter_by(**params)\
            .update(sql)
    return count


def downloads_plus(channel, **kwargs):
    channels = {
        DownloadChannelEnum.online: downloads_plus_by_online
    }
    try:
        if isinstance(channel, int) or str.isnumeric(channel):
            channel = int(channel)
            channel = DownloadChannelEnum(channel)
        else:
            channel = DownloadChannelEnum[channel]
    except ValueError:
        raise ParamException(error='the channel parameter is not in range')

    return channels.get(channel)(**kwargs)

