__author__ = 'bliss'

from herovii.libs.enums import MobileRace
from herovii.models.onlines.statistic import Statistic
from herovii.models.base import db
from herovii.libs.enums import DownloadChannel


def downloads_plus_byonline(**kwargs):
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
        DownloadChannel.online: downloads_plus_byonline
    }
    if str.isnumeric(channel):
        channel = int(channel)
        key = DownloadChannel(channel)
    else:
        key = DownloadChannel[channel]
    return channels.get(key)(**kwargs)

