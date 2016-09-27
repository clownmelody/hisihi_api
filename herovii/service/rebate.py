# -*- coding: utf-8 -*-
import time

from sqlalchemy import or_
from herovii.models.base import db
from herovii.libs.util import convert_paginate
from herovii.models.org.rebate import Rebate
from herovii.models.user.user_rebate import UserRebate
from herovii.models.org.teaching_course import TeachingCourse
from herovii.models.user.user_rebate_gift import UserRebateGift
from herovii.models.tag import Tag
from herovii.models.org.org_teaching_course_rebate_relation import OrgTeachingCourseRebateRelation
from herovii.models.org.gift_package import GiftPackage

__author__ = 'shaolei'


def get_rebate_list_by_uid(uid, type, page, per_page):
    start, stop = convert_paginate(int(page), int(per_page))
    # 返回已失效抵扣券
    if type:
        cur_time = int(time.time())
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
        cur_time = int(time.time())
        out_date_rebate = db.session.query(Rebate.id)\
            .filter(Rebate.use_end_time >= cur_time) \
            .all()
        out_date_rebate_ids = []
        for obj in out_date_rebate:
            out_date_rebate_ids.append(obj.id)
        rebate_list = db.session.query(UserRebate)\
            .filter(UserRebate.uid == uid, UserRebate.status == 0, UserRebate.rebate_id.in_(out_date_rebate_ids)) \
            .order_by(UserRebate.create_time.desc()) \
            .slice(start, stop).all()
        total_count = db.session.query(UserRebate).filter(UserRebate.uid == uid, UserRebate.status == 0).count()

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
    cur_time = int(time.time())
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
    tccr = db.session.query(OrgTeachingCourseRebateRelation.gift_package_id).filter(
        OrgTeachingCourseRebateRelation.teaching_course_id == user_rebate.teaching_course_id,
        OrgTeachingCourseRebateRelation.rebate_id == user_rebate.rebate_id,
        OrgTeachingCourseRebateRelation.status == 1) \
        .first()
    if tccr.gift_package_id:
        is_bind_gift_package = 1
    else:
        is_bind_gift_package = 0
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
        'is_obtain_gift_package': obtain_gift_package,
        'is_bind_gift_package': is_bind_gift_package
    }
    return rebate_obj


def get_rebate_detail_info(id):
    user_rebate = db.session.query(UserRebate).filter(UserRebate.id == id, UserRebate.status >= 0) \
        .order_by(UserRebate.create_time.desc()) \
        .first()
    rebate = db.session.query(Rebate).filter(Rebate.id == user_rebate.rebate_id).one()
    course = TeachingCourse.query.get(user_rebate.teaching_course_id)
    org_tag = db.session.query(Tag).filter(Tag.type == 5, Tag.status == 1) \
        .first()
    gift_package_info = get_gift_package_info_by_course_id_and_rebate_id(user_rebate.teaching_course_id,
                                                                         user_rebate.rebate_id)

    is_used = user_rebate.status
    cur_time = int(time.time())
    if cur_time > rebate.use_end_time:
        is_out_of_date = 1
    else:
        is_out_of_date = 0
    is_obtain_gift_package = db.session.query(UserRebateGift) \
        .filter(UserRebateGift.uid == user_rebate.uid,
                UserRebateGift.user_rebate_id == id,
                UserRebateGift.status != -1).count()
    if is_obtain_gift_package:
        obtain_gift_package = 1
    else:
        obtain_gift_package = 0
    rebate_text = str(rebate.value) + '元抵扣券抵' + str(rebate.rebate_value) + '元学费'
    rebate_info = {
        'user_rebate_id': id,
        'id': rebate.id,
        'use_start_time': rebate.use_start_time,
        'use_end_time': rebate.use_end_time,
        'value': rebate.value,
        'rebate_value': rebate.rebate_value,
        'rebate_text': rebate_text,
        'courses_name': course.course_name,
        'courses_id': course.id,
        'courses_pic': course.cover_pic,
        'is_out_of_date': is_out_of_date,
        'is_use': is_used,
        'promo_code': user_rebate.promo_code,
        'promo_code_url': user_rebate.promo_code_url,
        'use_condition': rebate.use_condition,
        'use_method': rebate.use_method,
        'use_instruction': rebate.use_instruction,
        'organization_id': course.organization_id,
        'customer_service_telephone_number': org_tag.value,
        'gift_package_info': gift_package_info,
        'name': rebate.name,
        'is_obtain_gift_package': obtain_gift_package,
        'order_id': user_rebate.order_id
    }
    return rebate_info


def get_gift_package_info_by_course_id_and_rebate_id(course_id, rebate_id):
    tccr = db.session.query(OrgTeachingCourseRebateRelation).filter(
        OrgTeachingCourseRebateRelation.teaching_course_id == course_id,
        OrgTeachingCourseRebateRelation.rebate_id == rebate_id,
        OrgTeachingCourseRebateRelation.status == 1) \
        .first()
    if tccr:
        gift_package_id = tccr.gift_package_id
        gift = db.session.query(GiftPackage).filter(
            GiftPackage.id == gift_package_id,
            GiftPackage.status == 1) \
            .first()
        if gift:
            return {
                'id': gift.id,
                'introduce': gift.introduce,
                'detail': gift.detail
            }
        else:
            return None
    else:
        return None
