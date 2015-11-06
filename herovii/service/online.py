__author__ = 'bliss'

from herovii.models.base import db
from herovii.models.onlines.statistic import Statistic


def pv_added_1(oid):
    sql = {Statistic.pv: Statistic.pv+1}
    with db.auto_commit():
        count = Statistic.query.filter_by(f_online_id=oid)\
            .update(sql)
    return count


def share_added_1(oid):
    sql = {Statistic.share: Statistic.share+1}
    with db.auto_commit():
        count = Statistic.query.filter_by(f_online_id=oid)\
            .update(sql)
    return count

