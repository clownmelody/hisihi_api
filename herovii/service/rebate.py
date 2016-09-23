# -*- coding: utf-8 -*-
import time

from sqlalchemy import or_
from herovii.models.base import db
from herovii.libs.util import convert_paginate
from herovii.models.org.rebate import Rebate
from herovii.models.user.user_rebate import UserRebate
from herovii.models.org.teaching_course import TeachingCourse
from herovii.models.user.user_rebate_gift import UserRebateGift

__author__ = 'shaolei'


def get_rebate_list_by_uid(uid, type, page, per_page):
    start, stop = convert_paginate(int(page), int(per_page))
    # 返回已失效抵扣券
    if type:
        cur_time = time.time()
        out_date_rebate = db.session.query(Rebate.id)\
            .filter(Rebate.use_end_time < cur_time) \
            .all()
        out_date_rebate_ids = []
        for obj in out_date_rebate:
            out_date_rebate_ids.append(obj.id)
        rebate_list = db.session.query(UserRebate)\
            .filter(UserRebate.uid == uid, or_(UserRebate.status == 1, UserRebate.rebate_id.in_(out_date_rebate_ids))) \
            .order_by(UserRebate.create_time.desc()) \
            .slice(start, stop).all()
        total_count = db.session.query(UserRebate)\
            .filter(UserRebate.uid == uid, or_(UserRebate.status == 1, UserRebate.rebate_id.in_(out_date_rebate_ids))) \
            .count()
        if rebate_list:
            rebate_info_list = []
            for rebate in rebate_list:
                rebate_info = get_rebate_info(rebate)
                rebate_info_list.append(rebate_info)
        else:
            total_count = 0
            rebate_info_list = None
    else:
        total_count = db.session.query(UserRebate).filter(UserRebate.uid == uid, UserRebate.status == 0).count()
        rebate_list = db.session.query(UserRebate).filter(UserRebate.uid == uid, UserRebate.status == 0) \
            .order_by(UserRebate.create_time.desc()) \
            .slice(start, stop).all()
        if rebate_list:
            rebate_info_list = []
            for rebate in rebate_list:
                rebate_info = get_rebate_info(rebate)
                rebate_info_list.append(rebate_info)
        else:
            total_count = 0
            rebate_info_list = None
    return total_count, rebate_info_list


def get_rebate_info(user_rebate):
    courses = db.session.query(TeachingCourse.course_name, TeachingCourse.cover_pic)\
        .filter(TeachingCourse.id == user_rebate.teaching_course_id)\
        .first()
    rebate = db.session.query(Rebate.name, Rebate.value, Rebate.rebate_value,
                              Rebate.use_start_time, Rebate.use_end_time)\
        .filter(Rebate.id == user_rebate.rebate_id)\
        .first()
    is_use = user_rebate.status
    user_rebate_id = user_rebate.id
    cur_time = time.time()
    if cur_time > rebate.use_end_time:
        is_out_of_date = 1
    else:
        is_out_of_date = 0
    is_obtain_gift_package = db.session.query(UserRebateGift) \
        .filter(UserRebateGift.uid == user_rebate.uid,
                UserRebateGift.user_rebate_id == user_rebate_id,
                UserRebateGift.status != -1).count()
    if is_obtain_gift_package:
        obtain_gift_package = 1
    else:
        obtain_gift_package = 0
    rebate_obj = {
        'id': user_rebate.rebate_id,
        'name': rebate.name,
        'use_start_time': rebate.use_start_time,
        'use_end_time': rebate.use_end_time,
        'value': rebate.value,
        'rebate_value': rebate.rebate_value,
        'courses_id': user_rebate.teaching_course_id,
        'courses_name': courses.course_name,
        'courses_pic': courses.cover_pic,
        'is_use': is_use,
        'is_out_of_date': is_out_of_date,
        'user_rebate_id': user_rebate_id,
        'is_obtain_gift_package': obtain_gift_package
    }
    return rebate_obj

