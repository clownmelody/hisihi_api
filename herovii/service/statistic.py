__author__ = 'bliss'

from herovii.libs.enums import MobileRace
from herovii.models.onlines.statistic import Statistic
from herovii.models.base import db


def downloads_plus_1(oid, type):
    types = {MobileRace.android: 'ddd'}
    statistic = Statistic()
    a=Statistic.query.filter_by(f_online_id=oid).first().android_downloads
    b=Statistic.query.filter_by(f_online_id=oid).first().ipad_downloads
    print(a,b)
    with db.auto_commit():
        statistic.query.filter_by(f_online_id=oid).update({
            Statistic.ipad_downloads: Statistic.ipad_downloads + 1
            })

