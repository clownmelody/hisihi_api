# -*- coding: utf-8 -*-
import time


from herovii.models.base import db
from herovii.libs.util import convert_paginate
from herovii.models.org.rebate import Rebate
from herovii.models.user.user_rebate import UserRebate
from herovii.models.org.teaching_course import TeachingCourse

__author__ = 'shaolei'


def get_rebate_list_by_uid(uid, page, per_page):
    start, stop = convert_paginate(int(page), int(per_page))
    total_count = db.session.query(UserRebate).filter(UserRebate.uid == uid, UserRebate.status > 0).count()
    coupon_list = db.session.query(UserRebate).filter(UserRebate.uid == uid, UserRebate.status > 0) \
        .order_by(UserRebate.create_time.asc()) \
        .slice(start, stop).all()
    coupon_info_list = []
    for coupon in coupon_list:
        info = db.session.query(Rebate).filter(Rebate.id == coupon.coupon_id).one()
        course = TeachingCourse.query.get(coupon.teaching_course_id)
        # is_used = is_coupon_used(info.id, uid, coupon.teaching_course_id)
        # is_out_of_date = is_coupon_out_of_date(info.id)
        # is_invalid = is_coupon_invalid(info.id, coupon.teaching_course_id)
        coupon_info = {
            'obtain_id': coupon.id,
            'id': info.id,
            'type': info.type,
            'start_time': info.start_time,
            'end_time': info.end_time,
            'money': info.money,
            'course_name': course.course_name,
            # 'is_out_of_date': is_out_of_date,
            # 'is_used': is_used,
            # 'is_invalid': is_invalid
        }
        coupon_info_list.append(coupon_info)
    return total_count, coupon_info_list



