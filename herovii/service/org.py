import string
from _operator import or_, and_
import re

import time
from datetime import datetime

from flask import json, current_app
from sqlalchemy.sql.expression import text, distinct
from sqlalchemy.sql.functions import func
from werkzeug.datastructures import MultiDict
from herovii.libs.error_code import NotFound, DataArgumentsException, StuClassNotFound, DirtyDataError, UpdateDBError, \
    ParamException
from herovii.libs.helper import get_full_oss_url, make_a_coupon_code, make_a_qrcode
from herovii.libs.util import get_today_string, convert_paginate
from herovii.models.base import db
from herovii.models.issue import Issue
from herovii.models.org.class_mirror import ClassMirror
from herovii.models.org.classmate import Classmate
from herovii.models.org.coupon import Coupon
from herovii.models.org.course import Course
from herovii.models.org.enroll import Enroll
from herovii.models.org.info import Info
from herovii.models.org.org_admin_bind_weixin import OrgAdminBindWeixin
from herovii.models.org.org_authentication import OrgAuthentication
from herovii.models.org.org_authentication_config import OrgAuthenticationConfig
from herovii.models.org.org_config import OrgConfig
from herovii.models.org.org_teaching_course_promotion_relation import OrgTeachingCoursePromotionRelation
from herovii.models.org.org_tag_relation import OrgTagRelation
from herovii.models.org.pic import Pic
from herovii.models.org.promotion import Promotion
from herovii.models.org.sign_in import StudentSignIn
from herovii.models.org.student_class import StudentClass
from herovii.models.org.teacher_group import TeacherGroup
from herovii.models.org.teacher_group_relation import TeacherGroupRelation
from herovii.models.org.teaching_course import TeachingCourse
from herovii.models.org.teaching_course_coupon_relation import TeachingCourseCouponRelation
from herovii.models.org.teaching_course_enroll import TeachingCourseEnroll
from herovii.models.org.video import Video
from herovii.models.overseas.organization_to_university import OrganizationToUniversity
from herovii.models.overseas.university import University
from herovii.models.tag import Tag
from herovii.models.user.field import Field
from herovii.models.user.avatar import Avatar
from herovii.models.user.follow import Follow
from herovii.models.user.id_realeation import IdRelation
from herovii.models.user.user_coupon import UserCoupon
from herovii.models.user.user_csu import UserCSU
from herovii.models.user.user_csu_secure import UserCSUSecure
from herovii.models.user.user_gift_package import UserGiftPackage
from herovii.service.file import FilePiper

__author__ = 'bliss'


def create_org_info(org):
    with db.auto_commit():
        db.session.add(org)
    return org


def get_org_teachers_by_group(oid):
    # collection = db.session.query(o.uid, TeacherGroupRelation.teacher_group_id,
    #                               TeacherGroup.title).\
    #     outerjoin(TeacherGroup, TeacherGroup.id == TeacherGroupRelation.teacher_group_id).filter(
    #     TeacherGroup.organization_id == oid, TeacherGroup.status != -1, TeacherGroupRelation.status != -1).\
    #     all()

    # relation = aliased
    # 这里需要使用子查询 subquery
    sub_query = db.session.query(TeacherGroupRelation). \
        filter(TeacherGroupRelation.status != -1).subquery()

    # 需要使用subquery的.c 属性来引用字段
    collection_query = db.session.query(TeacherGroup.id, TeacherGroup.title, sub_query.c.uid,
                                        sub_query.c.teacher_good_at_subjects, sub_query.c.teacher_introduce, ). \
        filter(TeacherGroup.organization_id == oid, TeacherGroup.status != -1). \
        outerjoin(sub_query, TeacherGroup.id == sub_query.c.teacher_group_id). \
        order_by(TeacherGroup.id)

    # collection_query = db.session.query(TeacherGroup.id, TeacherGroup.title, TeacherGroupRelation.uid).filter(
    #     TeacherGroup.organization_id == oid, TeacherGroup.status != -1).\
    #     outerjoin(TeacherGroupRelation, TeacherGroup.id == TeacherGroupRelation.teacher_group_id).\
    #     filter(TeacherGroupRelation.status != -1)

    s = collection_query.statement
    collection = collection_query.all()

    m = map(lambda x: x[2], collection)
    l = list(m)
    if not l:
        raise NotFound(error='organization not found', error_code=5004)

    # 下面的group_by 是为了去重，部分用户在avatar表有2个以上的头像
    teachers = db.session.query(UserCSU, Avatar.path). \
        outerjoin(Avatar, UserCSU.uid == Avatar.uid).filter(UserCSU.uid.in_(l), UserCSU.status != -1). \
        group_by(UserCSU.uid).all()

    return dto_teachers_group_1(oid, collection, teachers)


def get_org_teachers(oid, page, per_page):
    start = (page - 1) * per_page
    stop = start + per_page
    total_count = db.session.query(TeacherGroupRelation).filter(TeacherGroupRelation.group == 6,
                                                                TeacherGroupRelation.status == 1,
                                                                TeacherGroupRelation.organization_id == oid).count()
    teacher_list = db.session.query(TeacherGroupRelation).filter(TeacherGroupRelation.group == 6,
                                                                 TeacherGroupRelation.status == 1,
                                                                 TeacherGroupRelation.organization_id == oid).slice(
        start,
        stop) \
        .all()
    data = []
    for teacher in teacher_list:
        uid = teacher.uid
        user = db.session.query(UserCSU).filter(UserCSU.uid == uid).first()
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == uid).first()
        stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        tea_object = {
            'uid': teacher.uid,
            'teacher_group_id': teacher.teacher_group_id,
            'nickname': user.nickname,
            'avatar': stu_avatar_full_path,
            'teacher_good_at_subjects': teacher.teacher_good_at_subjects,
            'teacher_introduce': teacher.teacher_introduce
        }
        data.append(tea_object)
    return total_count, data


def dto_teachers_group(oid, l, teachers):
    # groups = []
    group_keys = {}
    for t, avatar in teachers:
        avatar = get_full_oss_url(avatar, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        t = {'lecture': t, 'avatar': avatar}
        for uid, group_id, title in l:
            if uid == t['lecture'].uid:
                if group_keys.get(group_id):
                    group_keys[group_id]['lectures'].append(t)
                    # group_keys.append(group_id)

                else:
                    group = {
                        'group_id': group_id,
                        'group_title': title,
                        'lectures': [t]
                    }
                    group_keys[group_id] = group

    groups = tuple(group_keys.values())

    return {
        'org_id': oid,
        'groups': groups
    }


def dto_teachers_group_1(oid, l, teachers):
    group_keys = MultiDict()
    for group_id, title, uid, teacher_good_at_subjects, teacher_introduce in l:
        group_keys.add((group_id, title), (uid, teacher_good_at_subjects, teacher_introduce))

    groups = []

    for key in group_keys.keys():
        uids = group_keys.getlist(key)
        group = {
            'group_id': key[0],
            'group_title': key[1]
        }
        lectures = []
        for uid in uids:
            for t, avatar in teachers:
                if uid[0] == t.uid:
                    avatar = get_full_oss_url(avatar, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
                    t = {'lecture': t, 'avatar': avatar, 'teacher_good_at_subjects': uid[1],
                         'teacher_introduce': uid[2]}
                    lectures.append(t)
        group['lectures'] = lectures
        groups.append(group)
    groups = sorted(groups, key=lambda g: g['group_id'])
    return {
        'org_id': oid,
        'groups': groups
    }


def dto_org_courses_paginate(oid, page, count):
    courses_categories, total_count = get_org_courses_paging(oid, int(page), int(count))
    if not courses_categories:
        raise NotFound(error='courses not found', error_code=5002)
    m = map(lambda x: x[0].lecturer, courses_categories)
    l = list(m)
    teachers = UserCSU.query.filter(UserCSU.uid.in_(l)).all()
    c_l = []
    for c, category in courses_categories:
        if c['img_str'].startswith('OSS-'):
            c.img_str = c['img_str'].replace('OSS-', 'http://game-pic.oss-cn-qingdao.aliyuncs.com/')

        course = {
            'course': c,
            'category': category
        }

        for t in teachers:
            if t.uid == c.lecturer:
                course['lecture'] = t
        c_l.append(course)
    return {
        'organization_id': oid,
        'total_count': total_count,
        'courses': c_l
    }


def dto_org_teaching_courses_paginate(oid, except_id, page, count):
    teaching_courses_lsit, total_count = get_org_teaching_courses_paging(oid, except_id, int(page), int(count))
    if not teaching_courses_lsit:
        raise NotFound(error='teaching courses not found', error_code=5008)
    c_l = []
    for course in teaching_courses_lsit:
        org_info = Info.query.get(oid)
        if not org_info:
            raise NotFound(error='organization not found')
        course = {
            'id': course.id,
            'organization_id': course.organization_id,
            'organization_name': org_info.name,
            'course_name': course.course_name,
            'cover_pic': course.cover_pic,
            'start_course_time': course.start_course_time,
            'end_course_time': course.end_course_time,
            'lesson_period': course.lesson_period,
            'student_num': course.student_num,
            'lecture_name': course.lecture_name,
            'price': course.price,
            'already_registered': course.already_registered
        }
        c_l.append(course)
    return {
        'total_count': total_count,
        'courses': c_l
    }


def dto_org_teaching_courses_paginate_v2_9(oid, except_id, page, count, uid):
    teaching_courses_lsit, total_count = get_org_teaching_courses_paging(oid, except_id, int(page), int(count))
    if not teaching_courses_lsit:
        raise NotFound(error='teaching courses not found', error_code=5008)
    c_l = []
    for course in teaching_courses_lsit:
        org_info = Info.query.get(oid)
        if not org_info:
            raise NotFound(error='organization not found')
        coupon = get_teaching_course_promotions_by_id(course.id, uid)
        course = {
            'id': course.id,
            'organization_id': course.organization_id,
            'organization_name': org_info.name,
            'course_name': course.course_name,
            'cover_pic': course.cover_pic,
            'start_course_time': course.start_course_time,
            'end_course_time': course.end_course_time,
            'lesson_period': course.lesson_period,
            'student_num': course.student_num,
            'lecture_name': course.lecture_name,
            'price': course.price,
            'already_registered': course.already_registered,
            'coupon_list': coupon
        }
        c_l.append(course)
    return {
        'total_count': total_count,
        'courses': c_l
    }


def get_org_courses_paging(oid, page, count):
    # q = Course.query.filter_by(organization_id=oid)
    # courses = q.paginate(page, count).items
    q = db.session.query(Course, Issue).filter(
        Course.status != -1, Issue.status != -1, Course.organization_id == oid
    ).join(Issue, Course.category_id == Issue.id).group_by(Course.create_time.desc())
    total_count = q.count()
    start, stop = convert_paginate(page, count)
    courses = q.slice(start, stop).all()
    return courses, total_count


def get_org_teaching_courses_paging(oid, except_id, page, count):
    start, stop = convert_paginate(page, count)
    total_count = db.session.query(TeachingCourse).filter(
        TeachingCourse.status == 1,
        TeachingCourse.id != except_id,
        TeachingCourse.organization_id == oid) \
        .count()
    teaching_course_list = db.session.query(TeachingCourse).filter(
        TeachingCourse.status == 1,
        TeachingCourse.id != except_id,
        TeachingCourse.organization_id == oid) \
        .slice(start, stop) \
        .all()
    return teaching_course_list, total_count


def get_course_by_id(cid):
    course = Course.query.get(cid)
    if not course:
        raise NotFound(error_code=5002, error='课程信息不存在')
    teacher = UserCSU.query.filter_by(uid=course.lecturer).first()
    videos = get_video_by_course_id(cid)
    issue = Issue.query.filter_by(id=course.category_id).first()
    return {
        'course': course,
        'teacher': teacher,
        'videos': videos,
        'category': issue
    }


def get_teaching_course_by_id(cid):
    course = TeachingCourse.query.get(cid)
    if not course:
        raise NotFound(error_code=5008, error='培训课程信息不存在')
    org_info = Info.query.get(course.organization_id)
    if not org_info:
        raise NotFound(error='organization not found')
    server_host_name = current_app.config['SERVER_HOST_NAME']
    web_url = server_host_name + "/api.php?s=/organization/showteachingcoursemainpage/course_id/" + str(cid)
    return {
        'course_id': cid,
        'organization_id': course.organization_id,
        'organization_name': org_info.name,
        'course_name': course.course_name,
        'cover_pic': course.cover_pic,
        'start_course_time': course.start_course_time,
        'end_course_time': course.end_course_time,
        'lesson_period': course.lesson_period,
        'student_num': course.student_num,
        'lecture_name': course.lecture_name,
        'price': course.price,
        'web_url': web_url
    }


def get_teaching_course_by_id_v2_9(cid):
    course = TeachingCourse.query.get(cid)
    if not course:
        raise NotFound(error_code=5008, error='培训课程信息不存在')
    org_info = Info.query.get(course.organization_id)
    if not org_info:
        raise NotFound(error='organization not found')
    server_host_name = current_app.config['SERVER_HOST_NAME']
    web_url = server_host_name + "/api.php?s=/organization/showteachingcoursemainpage_v2_9/course_id/" + str(cid)
    return {
        'course_id': cid,
        'organization_id': course.organization_id,
        'organization_name': org_info.name,
        'course_name': course.course_name,
        'cover_pic': course.cover_pic,
        'start_course_time': course.start_course_time,
        'end_course_time': course.end_course_time,
        'lesson_period': course.lesson_period,
        'student_num': course.student_num,
        'lecture_name': course.lecture_name,
        'price': course.price,
        'web_url': web_url
    }


def get_teaching_course_detail_by_id(cid):
    course = TeachingCourse.query.get(cid)
    if not course:
        raise NotFound(error_code=5008, error='培训课程信息不存在')
    org_info = Info.query.get(course.organization_id)
    if not org_info:
        raise NotFound(error='organization not found')
    total_count, enroll_list = get_teaching_course_enroll_by_id(cid, 1, 2000)
    return {
        'organization_id': course.organization_id,
        'organization_name': org_info.name,
        'course_name': course.course_name,
        'cover_pic': course.cover_pic,
        'start_course_time': course.start_course_time,
        'end_course_time': course.end_course_time,
        'lesson_period': course.lesson_period,
        'student_num': course.student_num,
        'lecture_name': course.lecture_name,
        'price': course.price,
        'already_registered': course.already_registered,
        'light_authentication': org_info.light_authentication,
        'introduction': course.introduction,
        'plan': course.plan,
        'enroll_info': {
            "total_count": total_count,
            "data": enroll_list
        }
    }


def get_teaching_course_enroll_by_id(cid, page, per_page):
    start, stop = convert_paginate(int(page), int(per_page))
    course = TeachingCourse.query.get(cid)
    if not course:
        raise NotFound(error_code=5008, error='培训课程信息不存在')
    total_count = TeachingCourseEnroll.query.filter_by(course_id=cid, status=1).count()
    enroll_list = TeachingCourseEnroll.query.filter_by(course_id=cid, status=1).slice(start, stop).all()
    enroll_user_list = []
    for enroll in enroll_list:
        user_info = UserCSU.query.filter_by(uid=enroll.uid).first()
        user_info = {
            'uid': user_info.uid,
            'nickname': user_info.nickname,
            'student_phone_num': enroll.student_phone_num,
            'create_time': enroll.create_time
        }
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == enroll.uid).first()
        if stu_avatar:
            stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
            user_info.setdefault('avatar', stu_avatar_full_path)
        enroll_user_list.append(user_info)
    return total_count, enroll_user_list


def get_video_by_course_id(cid):
    videos = Video.query.filter_by(course_id=cid, status=1).all()
    return videos


def create_org_pics(pics):
    # print(pics)
    # with db.auto_commit():
    #     db.session.execute(
    #         Pic.__table__.insert(),
    #         [pic for pic in pics]
    #     )
    with db.auto_commit():
        for pic in pics:
            db.session.add(pic)
    return pics


def view_student_count(oid):
    """查找status=1（正在审核的学生）和status=2已经审核过的学生数量"""
    counts = db.session.query(Enroll.status, func.count('*')). \
        filter(Enroll.organization_id == oid, Enroll.status != -1). \
        group_by(Enroll.status). \
        having(or_(Enroll.status == 1, Enroll.status == 2)). \
        all()
    return counts


def view_sign_in_count(oid, form):
    # 分页查询签到统计信息，如果某天没有任何人签到，则结果不会包含这天的信息
    since = form.since.data
    end = form.end.data
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    start = (page - 1) * per_page
    stop = start + per_page
    time_line = ''
    if since and end:
        time_line = 'create_time >=' + since + ' and create_time <=' + end
    if since and not end:
        time_line = 'create_time >=' + since
    if not since and end:
        time_line = 'create_time <=' + end
    # 按时间轴统计签到人数
    counts = db.session.query(StudentSignIn.date, func.count('*')). \
        filter(StudentSignIn.organization_id == oid, text(time_line), StudentSignIn.status != -1). \
        order_by(StudentSignIn.date.desc()). \
        group_by(StudentSignIn.date). \
        slice(start, stop).all()

    # 获取符合条件的记录的总条数
    record_total_count = db.session.query(func.count(distinct(StudentSignIn.date))). \
        select_from(StudentSignIn). \
        filter(StudentSignIn.organization_id == oid, text(time_line), StudentSignIn.status != -1). \
        scalar()

    # 根据日期获取当日的总人数
    m = map(lambda x: x[0], counts)
    dates = list(m)
    total = db.session.query(ClassMirror.date, func.group_concat(ClassMirror.classmates)). \
        filter(ClassMirror.date.in_(dates)). \
        group_by(ClassMirror.date).slice(start, stop).all()

    m = map(lambda x: (x[0], len(re.split(',|#', x[1]))), total)
    total = dict(m)
    data = []
    for date, count in counts:
        total_count = total.get(date)
        if not total_count:
            total_count = 0
        sign_in_stats = {
            'date': date,
            'sign_in_count': count,
            'total_count': total_count,
        }
        data.append(sign_in_stats)
    dto = {
        'record_total_count': record_total_count,
        'sign_in_stats': data
    }
    return dto


def view_sign_in_count_single(oid, date):
    # 查询某一天的签到情况
    count = db.session.query(func.count('*')).select_from(StudentSignIn). \
        filter(StudentSignIn.organization_id == oid, StudentSignIn.status != -1, StudentSignIn.date == date). \
        scalar()
    if not count:
        raise NotFound()

    total = db.session.query(ClassMirror.class_id, func.group_concat(ClassMirror.classmates)).filter(
        ClassMirror.date == date). \
        group_by(ClassMirror.class_id).all()

    count_by_class = map(lambda x: len(re.split(',|#', x[1])), total)
    total_count = sum(list(count_by_class))
    data = {
        'date': date,
        'sign_in_count': count,
        'total_count': total_count
    }
    return data


def get_uid_sign_in_total_count_by_now(uid):
    count = db.session.query(func.count('*')).select_from(StudentSignIn). \
        filter(and_(StudentSignIn.uid == uid, StudentSignIn.status != -1)).scalar()
    return count


def get_org_by_id(oid):
    org_info = Info.query.get(oid)
    if not org_info:
        raise NotFound('org not found')
    return org_info


def get_org_by_uid(uid):
    org_info = Info.query.filter_by(uid=uid).first()
    if not org_info:
        raise NotFound('org not found')
    return org_info


# def test(url):
#     if url.startswith('http//')
#     return url

def dto_get_blzs_paginate(page, count, oid):
    # 可能会造成性能低下，尽量将筛选条件在第一次join时应用，以减少记录数
    # query里用到outerjoin是因为不希望在course为null的情况下造成没有查询结果
    # 使用outerjoin将保证即使没有课程，也可以筛选报名结果
    # 使用Enroll的blz_id订单号分组是为了去除重复（有些用户在avatar表里有2个以上的头像）
    blzs_query = db.session.query(
        Enroll, UserCSU.nickname, OrgConfig.value,
        Avatar.path
    ).filter(Enroll.organization_id == oid, Enroll.status != -1). \
        outerjoin(UserCSU, Enroll.student_uid == UserCSU.uid). \
        outerjoin(Avatar, Enroll.student_uid == Avatar.uid). \
        outerjoin(OrgConfig, Enroll.course_id == OrgConfig.id). \
        order_by(Enroll.create_time.desc()).group_by(Enroll.blz_id)
    s = blzs_query.statement

    blzs_query = blzs_query.offset((page - 1) * count)
    blzs_query = blzs_query.limit(count)
    blzs = blzs_query.all()
    dto_blzs = __assign_blzs(blzs)
    return dto_blzs


def get_blzs_total_count():
    total_count = db.session.query(func.count('*')).filter(Enroll.status != -1).scalar()
    return total_count


def __assign_blzs(blzs):
    dto_blz = []
    # func = lambda x, y: x if x[0]['blz_id'] == y[0]['blz_id'] else x+[y]
    # (func, [[], ] + blzs)
    for blz in blzs:
        # for blz_base, nickname, avatar in blz:
        data = {
            'blz': blz[0],
            'name': blz[1],
            'course': blz[2],
            'avatar': get_full_oss_url(blz[3], bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        }
        dto_blz.append(data)
    data = {
        'blzs': dto_blz,
        'total_count': get_blzs_total_count()
    }
    return data


def create_student_sign_in(oid, uid, date):
    sign_in = StudentSignIn.query.filter(
        StudentSignIn.date == date, StudentSignIn.uid == uid,
        StudentSignIn.organization_id == oid).first()

    if sign_in:
        # 如果已经签到，则不再重复签到
        return sign_in

    init_classmate_mirror(oid, date)

    with db.auto_commit():
        sign_in = StudentSignIn()
        sign_in.organization_id = oid
        sign_in.date = date
        sign_in.uid = uid
        db.session.add(sign_in)
    return sign_in


def init_classmate_mirror(oid, date):
    """每一天第一个人签到时，需要生成班级成员的镜像，作为历史记录"""
    today = get_today_string()
    has_inited = __class_mirror_inited(oid, today)
    if has_inited:
        # 如果镜像已经初始化则什么都不做
        return

    classes_uids = db.session.query(Classmate.class_id, Classmate.uid). \
        filter(Classmate.status == 1).order_by(Classmate.class_id).all()

    dicts = MultiDict(classes_uids)
    class_mirrors = []
    # key 就是 class_id
    for key in dicts.keys():
        uids = dicts.getlist(key)
        classmate_mirror = ClassMirror()
        classmate_mirror.organization_id = oid
        classmate_mirror.date = date
        classmate_mirror.class_id = key
        classmates_str = ''
        for uid in uids:
            classmates_str += str(uid) + '#'
        classmates_str = classmates_str[:-1]
        classmate_mirror.classmates = classmates_str
        class_mirrors.append(classmate_mirror)
    with db.auto_commit():
        db.session.add_all(class_mirrors)
    return class_mirrors


def add_classmate_mirror():
    pass


def __class_mirror_inited(oid, today):
    # 今天是否已经初始化了班级人员镜像
    classmate_mirror = ClassMirror.query.filter_by(
        organization_id=oid, date=today).first()
    if classmate_mirror:
        return True
    else:
        return False


def search_lecture(args):
    lid = args.get('lid')
    if lid:
        lecture = db.session.query(
            UserCSU, Avatar.path). \
            filter(UserCSU.uid == lid, UserCSU.status != -1). \
            outerjoin(Avatar, UserCSU.uid == Avatar.uid).first()
        return _filter_lecture_dto(lecture)

    mobile = args.get('mobile')
    if mobile:
        lecture = db.session.query(
            UserCSU, Avatar.path). \
            join(UserCSUSecure, UserCSUSecure.id == UserCSU.uid). \
            filter(UserCSUSecure.mobile == mobile, UserCSU.status != -1). \
            outerjoin(Avatar, UserCSU.uid == Avatar.uid).first()
        return _filter_lecture_dto(lecture)

    raise NotFound()


def _filter_lecture_dto(lecture):
    if not lecture:
        raise NotFound()
    lecture_temp = lecture[0]
    avatar = lecture[1]
    data = {
        'lecture': lecture_temp,
        'avatar': get_full_oss_url(avatar, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
    }
    return json.dumps(data)


def get_org_student_profile_by_uid(uid):
    u = db.session.query(Enroll).filter(Enroll.student_uid == uid).first()
    if u is not None:
        stu_course = db.session.query(OrgConfig).filter(OrgConfig.id == u.course_id).first()
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == uid).first()
        if stu_avatar:
            stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        else:
            stu_avatar_full_path = None
        stu_classmate = db.session.query(Classmate).filter(Classmate.uid == uid).first()
        stu_sign_in_count = get_uid_sign_in_total_count_by_now(uid)
        if stu_classmate is None:
            class_group = None
        else:
            class_info = db.session.query(StudentClass).filter(StudentClass.id == stu_classmate.class_id).first()
            if class_info is not None:
                class_group = class_info.title
                total_class_hour = get_student_class_hour(class_info)
        if stu_course is None:
            course_name = None
        else:
            course_name = stu_course.value
        data = {
            'uid': u.student_uid,
            'avatar': stu_avatar_full_path,
            'student_name': u.student_name,
            'course_name': course_name,
            'class_group': class_group,
            'sign_in_count': stu_sign_in_count,
            'graduation_status': stu_classmate.status,
            'class_id': stu_classmate.class_id,
            'total_class': total_class_hour
        }
    else:
        return None
    return data


def get_student_class_hour(class_info):
    week = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    week_class_hour_count = 7
    class_start_date = datetime.strptime(class_info.class_start_date, '%Y-%m-%d')
    class_end_date = datetime.strptime(class_info.class_end_date, '%Y-%m-%d')
    total_days = class_end_date - class_start_date
    total_days = total_days.days + 1
    if 0 < total_days < 8:
        end_day_in_week = -1
    elif total_days > 7:
        end_day_in_week = class_end_date.weekday()
    else:
        raise DirtyDataError()
    start_day_in_week = class_start_date.weekday()
    days_in_first_week = 7 - start_day_in_week
    days_in_last_week = end_day_in_week + 1
    class_days_in_first_week = days_in_first_week
    class_days_in_last_week = days_in_last_week
    for item in range(len(week)):
        if (class_info.__getitem__(week[item]) is None) \
                or (class_info.__getitem__(week[item]).strip() is ''):
            week_class_hour_count -= 1
            if start_day_in_week <= item < 7:
                class_days_in_first_week -= 1
            if 0 <= item <= end_day_in_week:
                class_days_in_last_week -= 1
    total_class_hour = ((total_days - days_in_first_week - days_in_last_week) / 7) * week_class_hour_count
    total_class_hour = int(total_class_hour) + class_days_in_first_week + class_days_in_last_week
    return total_class_hour


def get_user_profile_by_uid(uid):
    user = db.session.query(UserCSU).filter(UserCSU.uid == uid).first()
    if user:
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == uid).first()
        if stu_avatar:
            stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        else:
            stu_avatar_full_path = None
        data = {
            'uid': user.uid,
            'avatar': stu_avatar_full_path,
            'nickname': user.nickname,
        }
        return data
    else:
        return None


def get_org_student_sign_in_history_by_uid(uid, page, per_page):
    start = (page - 1) * per_page
    stop = start + per_page
    student_class = db.session.query(Classmate).filter(Classmate.uid == uid, Classmate.status == 1).first()
    if student_class is None:
        raise StuClassNotFound
    class_mirror_total_count = db.session.query(ClassMirror).filter(
        ClassMirror.class_id == student_class.class_id).count()
    class_mirror_list = db.session.query(ClassMirror).filter(ClassMirror.class_id == student_class.class_id) \
        .slice(start, stop) \
        .all()
    if class_mirror_list is None:
        return None
    sign_in_dto = []
    sign_in_count = 0
    for class_mirror in class_mirror_list:
        sign_in = db.session.query(StudentSignIn.uid, StudentSignIn.organization_id, StudentSignIn.date) \
            .filter(StudentSignIn.uid == uid, StudentSignIn.status != -1, StudentSignIn.date == class_mirror.date) \
            .order_by(StudentSignIn.sign_in_time.desc()) \
            .first()
        if sign_in is not None:
            sign_in_count += 1
            data = {
                'uid': uid,
                'is_sign_in': True,
                'date': class_mirror.date
            }
        else:
            data = {
                'uid': uid,
                'is_sign_in': False,
                'date': class_mirror.date
            }
        sign_in_dto.append(data)
    class_info = db.session.query(StudentClass).filter(StudentClass.id == student_class.class_id,
                                                       StudentClass.status == 1).first()
    student_class_hour = get_student_class_hour(class_info)
    completion_rate = int((sign_in_count / student_class_hour) * 100)
    completion_rate = str(completion_rate) + '%'
    return class_mirror_total_count, sign_in_dto, student_class_hour, completion_rate


def get_class_sign_in_detail_by_date(oid, cid, date, page, per_page):
    # 检查班级是否存在
    exist_class_in_org = db.session.query(StudentClass).filter(StudentClass.organization_id == oid,
                                                               StudentClass.status == 1,
                                                               StudentClass.id == cid).first()
    if exist_class_in_org:
        start = (page - 1) * per_page
        stop = start + per_page
        # 班级学生总数
        total_count = db.session.query(Classmate.uid). \
            filter(Classmate.status == 1, Classmate.class_id == cid). \
            order_by(Classmate.uid.desc()). \
            count()
        # 班级所有学生列表
        all_stu_list = db.session.query(Classmate.uid). \
            filter(Classmate.status == 1, Classmate.class_id == cid). \
            order_by(Classmate.uid.desc()).all()
        sign_in_count = 0
        sign_in_uid_list = []
        unsign_in_uid_list = []
        for _stu in all_stu_list:
            is_sign_in = db.session.query(StudentSignIn.id).filter(StudentSignIn.organization_id == oid,
                                                                   StudentSignIn.status == 1,
                                                                   StudentSignIn.uid == _stu.uid,
                                                                   StudentSignIn.date == date).first()
            if is_sign_in:
                sign_in_count += 1
                sign_in_uid_list.append(_stu.uid)
            else:
                unsign_in_uid_list.append(_stu.uid)
        stu_list = unsign_in_uid_list + sign_in_uid_list
        stu_list = stu_list[start:stop]
        data_list = []
        for _uid in stu_list:
            exist_sign_in = db.session.query(StudentSignIn.id).filter(StudentSignIn.organization_id == oid,
                                                                      StudentSignIn.status == 1,
                                                                      StudentSignIn.uid == _uid,
                                                                      StudentSignIn.date == date).first()
            user_info = db.session.query(UserCSU).filter(UserCSU.uid == _uid).first()
            stu_avatar = db.session.query(Avatar).filter(Avatar.uid == _uid).first()
            stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
            user = {"uid": _uid, 'avatar': stu_avatar_full_path, 'nickname': user_info.nickname}
            if exist_sign_in:
                user['sign_in_status'] = True
            else:
                user['sign_in_status'] = False
            data_list.append(user)
    else:
        raise DataArgumentsException()
    # 计算未签到数量
    unsign_in_count = total_count - sign_in_count
    return data_list, total_count, sign_in_count, unsign_in_count


def get_org_class_all_students_service(oid, cid, page, per_page):
    is_exist = db.session.query(StudentClass).filter(StudentClass.organization_id == oid,
                                                     StudentClass.id == cid,
                                                     StudentClass.status == 1) \
        .count()
    if not is_exist:
        raise ParamException()
    start = (page - 1) * per_page
    stop = start + per_page
    class_stu_total_count = db.session.query(Classmate).filter(Classmate.class_id == cid,
                                                               Classmate.status == 1) \
        .count()
    class_stu_list = db.session.query(Classmate.uid).filter(Classmate.class_id == cid,
                                                            Classmate.status == 1) \
        .slice(start, stop) \
        .all()
    data = []
    for stu in class_stu_list:
        user_info = db.session.query(UserCSU).filter(UserCSU.uid == stu.uid).first()
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == stu.uid).first()
        stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        user = {"uid": stu.uid, 'avatar': stu_avatar_full_path, 'nickname': user_info.nickname}
        data.append(user)
    return data, class_stu_total_count


def get_org_list_class_sign_in_count_stats(oid, date, page, per_page):
    start = (page - 1) * per_page
    stop = start + per_page
    # 分页获取机构的班级
    class_total_count = db.session.query(StudentClass).filter(StudentClass.organization_id == oid,
                                                              StudentClass.status == 1).count()
    class_list = db.session.query(StudentClass).filter(StudentClass.organization_id == oid,
                                                       StudentClass.status == 1). \
        slice(start, stop). \
        all()
    data_list = []
    for class_info in class_list:
        # 获取班级学生总数
        class_stu_total_count = db.session.query(Classmate).filter(Classmate.class_id == class_info.id,
                                                                   Classmate.status == 1).count()
        # 获取班级学生列表
        class_stu_list = db.session.query(Classmate).filter(Classmate.class_id == class_info.id,
                                                            Classmate.status == 1).all()
        sign_total_count = 0
        for stu in class_stu_list:
            # 获取班级学生的签到状态
            exist_sign_in = db.session.query(StudentSignIn.id).filter(StudentSignIn.organization_id == oid,
                                                                      StudentSignIn.status == 1,
                                                                      StudentSignIn.uid == stu.uid,
                                                                      StudentSignIn.date == date).first()
            if exist_sign_in:
                sign_total_count += 1
        data = {
            'class_id': class_info.id,
            'class_name': class_info.title,
            'stu_total_count': class_stu_total_count,
            'sign_total_count': sign_total_count
        }
        data_list.append(data)
    return class_total_count, data_list


def get_org_student_class_in(uid, oid):
    class_total_count = db.session.query(StudentClass).filter(StudentClass.organization_id == oid,
                                                              StudentClass.status == 1).count()
    all_class = db.session.query(StudentClass).filter(StudentClass.organization_id == oid,
                                                      StudentClass.status == 1).all()
    my_class = db.session.query(Classmate.class_id).filter(Classmate.uid == uid, Classmate.status == 1).first()
    data_list = []
    for class_item in all_class:
        data = {
            'class_id': class_item.id,
            'class_name': class_item.title
        }
        if class_item.id == my_class.class_id:
            data['in_this_class'] = True
        else:
            data['in_this_class'] = False
        data_list.append(data)
    return data_list, class_total_count


def get_graduated_student_service(oid, page, per_page):
    start = (page - 1) * per_page
    stop = start + per_page
    student_total_count = db.session.query(Classmate.uid).join(StudentClass, Classmate.class_id == StudentClass.id) \
        .filter(StudentClass.organization_id == oid, StudentClass.status == 1, Classmate.status == 2) \
        .count()
    student_list = db.session.query(Classmate.uid).join(StudentClass, Classmate.class_id == StudentClass.id) \
        .filter(StudentClass.organization_id == oid, StudentClass.status == 1, Classmate.status == 2) \
        .slice(start, stop) \
        .all()
    data_list = []
    for student in student_list:
        uid = student.uid
        user = db.session.query(UserCSU).filter(UserCSU.uid == uid).first()
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == uid).first()
        if stu_avatar:
            stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        stu_profile = {
            'uid': uid,
            'nickname': user.nickname,
            'avatar': stu_avatar_full_path
        }
        data_list.append(stu_profile)
    return data_list, student_total_count


def move_student_to(uid, class_id):
    count = db.session.query(Classmate).filter(Classmate.uid == uid).count()
    if not count:
        raise NotFound()
    res = db.session.query(Classmate).filter(Classmate.uid == uid).update({Classmate.class_id: class_id})
    if res:
        data = {
            "uid": uid,
            "class_id": class_id
        }
    return data


def update_stu_graduation_status(uid, class_id, status):
    pre_status = db.session.query(Classmate.status).filter(Classmate.uid == uid,
                                                           Classmate.class_id == class_id).first()
    if int(pre_status.status) < 1:
        raise DirtyDataError()
    res = db.session.query(Classmate).filter(Classmate.uid == uid, Classmate.class_id == class_id) \
        .update({Classmate.status: status})
    if res:
        data = {
            "uid": uid,
            "class_id": class_id,
            "status": status
        }
    else:
        raise UpdateDBError()
    return data


def get_org_pics(type_c, page, per_page, oid):
    page = int(page)
    per_page = int(per_page)
    start = (page - 1) * per_page
    stop = start + per_page

    if type_c != '0':
        type_str = 'type = ' + type_c
    else:
        type_str = ''

    pics = db.session.query(Pic).filter(Pic.organization_id == oid,
                                        Pic.status != -1, text(type_str)).order_by(Pic.create_time.desc()). \
        slice(start, stop).all()

    if not pics:
        raise NotFound(error_code=5007, error='the pics of this org are not found')

    total_count = db.session.query(func.count('*')).select_from(Pic). \
        filter(Pic.organization_id == oid, Pic.status != -1, text(type_str)).scalar()

    data = {
        'pics': pics,
        'total_count': total_count
    }
    return data


def set_lecturer_extend_info(uid, oid):
    res = db.session.query(IdRelation).filter(IdRelation.uid == uid) \
        .update({IdRelation.group_id: 6})
    org_name = db.session.query(Info.name).filter(Info.id == oid, Info.status == 1).first()
    count = db.session.query(Field).filter(Field.uid == uid, Field.field_id == 39).count()
    result = 0
    field = None
    if not count:
        field = Field()
        field.uid = uid
        field.field_id = 39
        field.field_data = org_name.name
        field.createTime = int(time.time())
        field.changeTime = int(time.time())
        with db.auto_commit():
            db.session.add(field)
    else:
        result = db.session.query(Field).filter(Field.uid == uid, Field.field_id == 39) \
            .update({Field.field_data: org_name.name})
    if res and (result or field.id):
        return True
    else:
        raise UpdateDBError()


def get_org_all_class_service(oid, page, per_page):
    class_total_count = db.session.query(StudentClass).filter(StudentClass.organization_id == oid,
                                                              StudentClass.status == 1).count()
    start = (page - 1) * per_page
    stop = start + per_page
    class_list = db.session.query(StudentClass.id, StudentClass.title, StudentClass.monday, StudentClass.tuesday,
                                  StudentClass.wednesday, StudentClass.thursday, StudentClass.friday,
                                  StudentClass.saturday, StudentClass.sunday) \
        .filter(StudentClass.organization_id == oid, StudentClass.status == 1) \
        .slice(start, stop) \
        .all()
    data = []
    for org_class in class_list:
        class_stu_total_count = db.session.query(Classmate).filter(Classmate.class_id == org_class.id,
                                                                   Classmate.status == 1).count()
        class_time = '周一' + parse_class_time(org_class.monday) + '、周二' + parse_class_time(org_class.tuesday) \
                     + '、周三' + parse_class_time(org_class.wednesday) + '、周四' + parse_class_time(org_class.thursday) \
                     + '、周五' + parse_class_time(org_class.friday) + '、周六' + parse_class_time(org_class.saturday) \
                     + '、周日' + parse_class_time(org_class.sunday)
        _org_class = {"id": org_class.id, "name": org_class.title, "student_count": class_stu_total_count,
                      "class_time": class_time}
        data.append(_org_class)
    return data, class_total_count


def parse_class_time(day):
    class_time = ''
    if day is None:
        day = ''
    if day.find('1') >= 0:
        class_time += '上'
    if day.find('2') >= 0:
        class_time += '下'
    if day.find('3') >= 0:
        class_time += '晚'
    if class_time is '':
        class_time += '无'
    return class_time


def get_org_enroll_student_service(oid, name):
    if name is None:
        enroll_students = db.session.query(Enroll.student_uid, UserCSU.nickname, Avatar.path) \
            .outerjoin(Avatar, Enroll.student_uid == Avatar.uid) \
            .outerjoin(UserCSU, Enroll.student_uid == UserCSU.uid) \
            .filter(Enroll.organization_id == oid, Enroll.status == 2) \
            .all()
        total_count = len(enroll_students)
    else:
        enroll_students = db.session.query(Enroll.student_uid, UserCSU.nickname, Avatar.path) \
            .outerjoin(Avatar, Enroll.student_uid == Avatar.uid) \
            .outerjoin(UserCSU, Enroll.student_uid == UserCSU.uid) \
            .outerjoin(UserCSUSecure, Enroll.student_uid == UserCSUSecure.id) \
            .filter(Enroll.organization_id == oid, Enroll.status == 2, or_(UserCSU.nickname.like('%' + name + '%'),
                                                                           UserCSUSecure.mobile.like('%' + name + '%'))) \
            .all()
        total_count = len(enroll_students)
    data = []
    for student in enroll_students:
        avatar = get_full_oss_url(student.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        org_student = {"uid": student.student_uid, "nickname": student.nickname, "avatar": avatar}
        data.append(org_student)
    return data, total_count


def get_org_class_info_service(cid):
    class_info = db.session.query(StudentClass.id, StudentClass.title, StudentClass.class_start_date,
                                  StudentClass.class_end_date, StudentClass.monday, StudentClass.tuesday,
                                  StudentClass.wednesday, StudentClass.thursday, StudentClass.friday,
                                  StudentClass.saturday, StudentClass.sunday) \
        .filter(StudentClass.id == cid, StudentClass.status == 1) \
        .first()
    if not class_info:
        raise NotFound()
    data = {
        "id": class_info.id,
        "title": class_info.title,
        "class_start_date": class_info.class_start_date,
        "class_end_date": class_info.class_end_date,
        "monday": class_info.monday,
        "tuesday": class_info.tuesday,
        "wednesday": class_info.wednesday,
        "thursday": class_info.thursday,
        "friday": class_info.friday,
        "saturday": class_info.saturday,
        "sunday": class_info.sunday
    }
    return data


def join_org_class_service(cid, uids):
    ids = uids.split(':')
    info = []
    id_in_class = db.session.query(Classmate.uid) \
        .filter(Classmate.class_id == cid, Classmate.uid.in_(ids)) \
        .all()
    for id_in in id_in_class:
        if str(id_in.uid) in ids:
            ids.remove(str(id_in.uid))
    for uid in ids:
        stu = {
            "uid": int(uid),
            "class_id": cid,
            "status": 1,
            "create_time": int(time.time())
        }
        info.append(stu)
    with db.auto_commit():
        result = db.session.execute(Classmate.__table__.insert(), info)
    msg = str(result.rowcount) + ' students has been joined'
    return msg


def quit_org_class_service(cid, uids):
    ids = uids.split(':')
    with db.auto_commit():
        count = db.session.query(Classmate).filter(Classmate.class_id == cid, Classmate.uid.in_(ids)) \
            .delete(synchronize_session=False)
    return count


def update_teachers_field_info(oid, org_name):
    teachers = db.session.query(TeacherGroupRelation.uid) \
        .filter(TeacherGroupRelation.organization_id == oid, TeacherGroupRelation.group == 6,
                TeacherGroupRelation.status > 0) \
        .distinct() \
        .all()
    t_ids = []
    for uid in teachers:
        t_ids.append(uid.uid)
    if t_ids:
        result = db.session.query(Field).filter(Field.uid.in_(t_ids), Field.field_id == 39) \
            .update({Field.field_data: org_name}, synchronize_session=False)
        if not result:
            raise UpdateDBError()


def set_user_auth_group_access(uid, group_id):
    res = db.session.query(IdRelation).filter(IdRelation.uid == uid) \
        .update({IdRelation.group_id: group_id})
    if res:
        return True
    else:
        raise UpdateDBError()


def get_organization_info_by_organization_id(organization_id):
    organization = db.session.query(Info).filter(Info.id == organization_id) \
        .first()
    return organization


def add_major_to_org(oid, major_id):
    ids = major_id.split(':')
    info = []
    result = db.session.query(OrgTagRelation).filter(OrgTagRelation.organization_id == oid,
                                                     OrgTagRelation.tag_type == 8) \
        .delete()
    for tid in ids:
        stu = {
            "organization_id": int(oid),
            "tag_id": tid,
            "tag_type": 8,
            "status": 1,
            "create_time": int(time.time())
        }
        info.append(stu)
    with db.auto_commit():
        result = db.session.execute(OrgTagRelation.__table__.insert(), info)
    msg = str(result.rowcount) + ' major has been added'
    return msg


def get_major_by_oid(oid):
    major = db.session.query(OrgTagRelation.tag_id, Tag.value).filter(OrgTagRelation.organization_id == oid,
                                                                      OrgTagRelation.tag_type == 8,
                                                                      OrgTagRelation.status == 1) \
        .join(Tag, Tag.id == OrgTagRelation.tag_id) \
        .all()
    result = {
        "organization_id": oid,
        "major_list": None
    }
    if major:
        major_list = []
        for item in major:
            major_obj = {
                "id": item.tag_id,
                "value": item.value
            }
            major_list.append(major_obj)
        result['major_list'] = major_list
    return result


def get_org_stat(oid):
    if oid:
        org_info = get_org_by_id(oid)
        enroll_count = db.session.query(Enroll) \
            .filter(Enroll.organization_id == oid, Enroll.status == 2) \
            .count()
        org = db.session.query(Info) \
            .filter(Info.id == oid) \
            .first()
        follow_count = db.session.query(Follow) \
            .filter(Follow.follow_who == oid, Follow.type == 2) \
            .count()
        follow_count += int(org.fake_fans_count)
        auth_list = db.session.query(OrgAuthenticationConfig) \
            .filter(OrgAuthenticationConfig.status == 1,
                    OrgAuthenticationConfig.flag == 0) \
            .all()
        auth_result_list = []
        for auth in auth_list:
            is_auth = db.session.query(OrgAuthentication) \
                .filter(OrgAuthentication.organization_id == oid,
                        OrgAuthentication.authentication_id == auth.id) \
                .first()
            auth_data = {
                'id': auth.id,
                'name': auth.name,
                'default_display': auth.default_display,
                'pic_url': auth.pic_url,
                'disable_pic_url': auth.disable_pic_url,
                'tag_pic_url': auth.tag_pic_url,
                'content': auth.content,
                'status': False
            }
            if is_auth:
                auth_data['status'] = True
            auth_result_list.append(auth_data)
        return {
            'view_count': org_info.view_count,
            'id': org_info.id,
            'name': org_info.name,
            'logo': org_info.logo,
            'enroll_count': enroll_count,
            'auth': auth_result_list,
            'follow_count': follow_count
        }
    if not oid:
        raise NotFound('organization not found', error_code=5000)


def get_university_by_oid(oid):
    university = db.session.query(OrganizationToUniversity.university_id, University.name) \
        .filter(OrganizationToUniversity.organization_id == oid, OrganizationToUniversity.teaching_course_id == 0,
                OrganizationToUniversity.status == 1) \
        .join(University, OrganizationToUniversity.university_id == University.id) \
        .all()
    result = {
        "organization_id": oid,
        "university_list": None
    }
    if university:
        major_list = []
        for item in university:
            major_obj = {
                "id": item.university_id,
                "name": item.name
            }
            major_list.append(major_obj)
        result['university_list'] = major_list
    return result


def link_org_to_university(oid, university_id):
    ids = university_id.split(':')
    info = []
    result = db.session.query(OrganizationToUniversity) \
        .filter(OrganizationToUniversity.organization_id == oid,
                OrganizationToUniversity.teaching_course_id == 0) \
        .delete()
    for tid in ids:
        stu = {
            "organization_id": int(oid),
            "teaching_course_id": 0,
            "university_id": tid,
            "status": 1,
            "create_time": int(time.time())
        }
        info.append(stu)
    with db.auto_commit():
        result = db.session.execute(OrganizationToUniversity.__table__.insert(), info)
    msg = str(result.rowcount) + ' university has been added'
    return msg


# 获取机构参与活动的列表
def get_org_promotion_list(oid):
    promotion_list = db.session.query(distinct(OrgTeachingCoursePromotionRelation.promotion_id)) \
        .filter(OrgTeachingCoursePromotionRelation.organization_id == oid,
                OrgTeachingCoursePromotionRelation.status == 1) \
        .all()
    id_list = []
    for ids in promotion_list:
        id_list.append(ids[0])
    result_list = []
    for pid in id_list:
        promotion_info = db.session.query(Promotion) \
            .filter(Promotion.id == pid) \
            .one()
        info = {
            'id': promotion_info.id,
            'organization_id': oid,
            'tag_url': promotion_info.tag_url,
            'title': promotion_info.title
        }
        result_list.append(info)
    return result_list


# 获取活动详情
def get_promotion_detail_service(pid):
    promotion_info = db.session.query(Promotion) \
        .filter(Promotion.id == pid) \
        .one()
    return {
        'id': promotion_info.id,
        'title': promotion_info.title,
        'logo_url': promotion_info.logo_url,
        'little_logo_url': promotion_info.little_logo_url,
        'tag_url': promotion_info.tag_url,
        'description': promotion_info.description,
        'type': promotion_info.type,
        'detail_web_url': current_app.config[
                              'SERVER_HOST_NAME'] + '/api.php?s=/Promotion/promotion_detail/promotion_id/' + str(pid)
    }


def get_org_promotion_detail_service(oid, pid):
    promotion_info = db.session.query(Promotion) \
        .filter(Promotion.id == pid) \
        .one()
    return {
        'id': promotion_info.id,
        'title': promotion_info.title,
        'logo_url': promotion_info.logo_url,
        'little_logo_url': promotion_info.little_logo_url,
        'tag_url': promotion_info.tag_url,
        'description': promotion_info.description,
        'type': promotion_info.type,
        'detail_web_url': current_app.config[
                              'SERVER_HOST_NAME'] + '/api.php?s=/Promotion/promotion_detail/promotion_id/' + str(
            pid) + '/organization_id/' + str(oid)
    }


def get_promotion_teaching_course_list_service(pid, uid):
    _list = db.session.query(OrgTeachingCoursePromotionRelation) \
        .filter(OrgTeachingCoursePromotionRelation.promotion_id == pid,
                OrgTeachingCoursePromotionRelation.status == 1) \
        .all()
    course_list = []
    for course in _list:
        info = get_teaching_course_by_id(course.teaching_course_id)
        coupon_info = db.session.query(Coupon).join(TeachingCourseCouponRelation,
                                                    TeachingCourseCouponRelation.coupon_id == Coupon.id) \
            .order_by(Coupon.money.desc()) \
            .filter(TeachingCourseCouponRelation.teaching_course_id == course.teaching_course_id,
                    TeachingCourseCouponRelation.status == 1, Coupon.status == 1) \
            .first()
        if coupon_info is not None:
            is_used = is_coupon_used(coupon_info.id, uid, course.teaching_course_id)
            is_obtain = is_coupon_obtained(coupon_info.id, uid, course.teaching_course_id)
            if is_obtain:
                obtain_id = get_coupon_obtain_id(coupon_info.id, uid, course.teaching_course_id)
            else:
                obtain_id = 0
            is_out_of_date = is_coupon_out_of_date(coupon_info.id)
            new_coupon = {
                'id': coupon_info.id,
                'name': coupon_info.name,
                'type': coupon_info.type,
                'start_time': coupon_info.start_time,
                'end_time': coupon_info.end_time,
                'money': coupon_info.money,
                'is_used': is_used,
                'is_obtain': is_obtain,
                'is_out_of_date': is_out_of_date,
                'obtain_id': obtain_id
            }
        else:
            new_coupon = None
        info['coupon_info'] = new_coupon
        course_list.append(info)
    return course_list


def get_org_promotion_teaching_course_list_service(oid, pid, uid):
    _list = db.session.query(OrgTeachingCoursePromotionRelation) \
        .filter(OrgTeachingCoursePromotionRelation.promotion_id == pid,
                OrgTeachingCoursePromotionRelation.organization_id == oid,
                OrgTeachingCoursePromotionRelation.status == 1) \
        .all()
    course_list = []
    for course in _list:
        info = get_teaching_course_by_id(course.teaching_course_id)
        coupon_info = db.session.query(Coupon).join(TeachingCourseCouponRelation,
                                                    TeachingCourseCouponRelation.coupon_id == Coupon.id) \
            .order_by(Coupon.money.desc()) \
            .filter(TeachingCourseCouponRelation.teaching_course_id == course.teaching_course_id,
                    TeachingCourseCouponRelation.status == 1, Coupon.status == 1) \
            .first()
        if coupon_info is not None:
            is_used = is_coupon_used(coupon_info.id, uid, course.teaching_course_id)
            is_obtain = is_coupon_obtained(coupon_info.id, uid, course.teaching_course_id)
            if is_obtain:
                obtain_id = get_coupon_obtain_id(coupon_info.id, uid, course.teaching_course_id)
            else:
                obtain_id = 0
            is_out_of_date = is_coupon_out_of_date(coupon_info.id)
            new_coupon = {
                'id': coupon_info.id,
                'name': coupon_info.name,
                'type': coupon_info.type,
                'start_time': coupon_info.start_time,
                'end_time': coupon_info.end_time,
                'money': coupon_info.money,
                'is_used': is_used,
                'is_obtain': is_obtain,
                'is_out_of_date': is_out_of_date,
                'obtain_id': obtain_id
            }
        else:
            new_coupon = None
        info['coupon_info'] = new_coupon
        course_list.append(info)
    return course_list


def is_coupon_used(cid, uid, tid):
    is_used = db.session.query(UserCoupon) \
        .filter(UserCoupon.coupon_id == cid,
                UserCoupon.uid == uid,
                UserCoupon.teaching_course_id == tid,
                UserCoupon.status == 2) \
        .count()
    if is_used:
        return True
    return False


def is_coupon_obtained(cid, uid, tid):
    is_used = db.session.query(UserCoupon) \
        .filter(UserCoupon.coupon_id == cid,
                UserCoupon.uid == uid,
                UserCoupon.teaching_course_id == tid,
                UserCoupon.status > 0) \
        .count()
    if is_used:
        return True
    return False


def get_coupon_obtain_id(cid, uid, tid):
    user_coupon = db.session.query(UserCoupon) \
        .filter(UserCoupon.coupon_id == cid,
                UserCoupon.uid == uid,
                UserCoupon.teaching_course_id == tid,
                UserCoupon.status > 0) \
        .one()
    return user_coupon.id


def is_coupon_out_of_date(cid):
    coupon = db.session.query(Coupon) \
        .filter(Coupon.id == cid) \
        .one()
    now = int(time.time())
    if now <= int(coupon.end_time):
        return False
    return True


def is_coupon_invalid(coupon_id, teaching_course_id):
    coupon = db.session.query(Coupon) \
        .filter(Coupon.id == coupon_id,
                Coupon.status == 1) \
        .count()
    course = db.session.query(TeachingCourse).filter(
        TeachingCourse.status == 1,
        TeachingCourse.id == teaching_course_id) \
        .count()
    tccr = db.session.query(TeachingCourseCouponRelation) \
        .filter(TeachingCourseCouponRelation.teaching_course_id == teaching_course_id,
                TeachingCourseCouponRelation.coupon_id == coupon_id,
                TeachingCourseCouponRelation.status == 1) \
        .count()
    if coupon and course and tccr:
        return False
    else:
        return True


def get_teaching_course_promotions_by_id(cid, uid):
    _list = db.session.query(OrgTeachingCoursePromotionRelation) \
        .filter(OrgTeachingCoursePromotionRelation.teaching_course_id == cid,
                OrgTeachingCoursePromotionRelation.status == 1) \
        .all()
    promotion_list = []
    for _info in _list:
        promotion_info = get_promotion_detail_service(_info['promotion_id'])
        _coupon = db.session.query(Coupon).join(TeachingCourseCouponRelation,
                                                TeachingCourseCouponRelation.coupon_id == Coupon.id) \
            .order_by(Coupon.money.desc()) \
            .filter(TeachingCourseCouponRelation.teaching_course_id == cid,
                    TeachingCourseCouponRelation.status == 1, Coupon.status == 1) \
            .slice(0, 1) \
            .first()
        obj = {
            'promotion_info': promotion_info
        }
        if _coupon is not None:
            is_used = is_coupon_used(_coupon.id, uid, cid)
            is_obtain = is_coupon_obtained(_coupon.id, uid, cid)
            is_out_of_date = is_coupon_out_of_date(_coupon.id)
            obj['coupon_info'] = {
                'id': _coupon.id,
                'type': _coupon.type,
                'name': _coupon.name,
                'start_time': _coupon.start_time,
                'end_time': _coupon.end_time,
                'money': _coupon.money,
                'is_used': is_used,
                'is_obtain': is_obtain,
                'is_out_of_date': is_out_of_date
            }
            if is_obtain:
                obtain_id = db.session.query(UserCoupon.id).filter(UserCoupon.teaching_course_id == cid,
                                                                   UserCoupon.uid == uid,
                                                                   UserCoupon.status > 0,
                                                                   UserCoupon.coupon_id == _coupon.id) \
                    .first()
                obj['coupon_info']['obtain_id'] = obtain_id.id
        else:
            obj['coupon_info'] = None
        promotion_list.append(obj)
    return promotion_list


def get_coupon_list_by_uid(uid, page, per_page):
    start, stop = convert_paginate(int(page), int(per_page))
    total_count = db.session.query(UserCoupon).filter(UserCoupon.uid == uid, UserCoupon.status > 0).count()
    coupon_list = db.session.query(UserCoupon).filter(UserCoupon.uid == uid, UserCoupon.status > 0) \
        .order_by(UserCoupon.create_time.asc()) \
        .slice(start, stop).all()
    coupon_info_list = []
    for coupon in coupon_list:
        info = db.session.query(Coupon).filter(Coupon.id == coupon.coupon_id).one()
        course = TeachingCourse.query.get(coupon.teaching_course_id)
        is_used = is_coupon_used(info.id, uid, coupon.teaching_course_id)
        is_out_of_date = is_coupon_out_of_date(info.id)
        is_invalid = is_coupon_invalid(info.id, coupon.teaching_course_id)
        coupon_info = {
            'obtain_id': coupon.id,
            'id': info.id,
            'type': info.type,
            'start_time': info.start_time,
            'end_time': info.end_time,
            'money': info.money,
            'course_name': course.course_name,
            'is_out_of_date': is_out_of_date,
            'is_used': is_used,
            'is_invalid': is_invalid
        }
        coupon_info_list.append(coupon_info)
    return total_count, coupon_info_list


def get_teaching_course_coupon_code_service(uid):
    coupon_code = make_a_coupon_code(uid)
    oss_url = current_app.config['WEIXIN_SERVER_HOST_NAME'] + '/scissor/index/index?coupon=' + coupon_code
    return coupon_code, oss_url


def get_coupon_detail_by_uid(id):
    coupon = db.session.query(UserCoupon).filter(UserCoupon.id == id, UserCoupon.status > 0) \
        .order_by(UserCoupon.create_time.desc()) \
        .first()
    info = db.session.query(Coupon).filter(Coupon.id == coupon.coupon_id).one()
    course = TeachingCourse.query.get(coupon.teaching_course_id)
    is_used = is_coupon_used(info.id, coupon.uid, coupon.teaching_course_id)
    is_out_of_date = is_coupon_out_of_date(info.id)
    is_obtain_gift_package = db.session.query(UserGiftPackage) \
        .filter(UserGiftPackage.uid == coupon.uid,
                UserGiftPackage.obtain_coupon_record_id == coupon.id,
                UserGiftPackage.status != -1).count()
    course_coupon = db.session.query(TeachingCourseCouponRelation) \
        .filter(TeachingCourseCouponRelation.coupon_id == info.id,
                TeachingCourseCouponRelation.teaching_course_id == course.id).one()
    coupon_info = {
        'obtain_id': coupon.id,
        'id': info.id,
        'type': info.type,
        'start_time': info.start_time,
        'end_time': info.end_time,
        'money': info.money,
        'course_name': course.course_name,
        'is_out_of_date': is_out_of_date,
        'is_used': is_used,
        'promo_code': coupon.promo_code,
        'promo_code_url': coupon.promo_code_url,
        'service_condition': course_coupon.service_condition,
        'using_method': course_coupon.using_method,
        'instructions_for_use': course_coupon.instructions_for_use
    }
    if is_obtain_gift_package:
        coupon_info['is_obtain_gift_package'] = 2
    elif int(coupon.status) == 2:
        coupon_info['is_obtain_gift_package'] = 1
    else:
        coupon_info['is_obtain_gift_package'] = 0
    return coupon_info


def get_org_info_by_admin_id(aid):
    org = db.session.query(Info.id, Info.name, Info.logo, Info.application_status) \
        .filter(Info.uid == aid, Info.status == 1).first()
    if org:
        org_info = {
            'id': org.id,
            'name': org.name,
            'logo': org.logo,
            'application_status': org.application_status
        }
        return org_info
    else:
        return None


def verify_coupon_code_service(weixin_account, coupon_code):
    data = {
        'is_verify': False,
        'is_bind': False,
        'has_teaching_course': False,
        'is_out_of_date': False,
        'is_used': False,
        'course_name': '',
        'money': 0
    }
    admin_bind_weixin = db.session.query(OrgAdminBindWeixin.id, OrgAdminBindWeixin.organization_id,
                                         OrgAdminBindWeixin.admin_id) \
        .filter(OrgAdminBindWeixin.weixin_account == weixin_account, OrgAdminBindWeixin.status == 1).first()
    if not admin_bind_weixin:
        return data
    coupon = db.session.query(UserCoupon.id, UserCoupon.coupon_id, UserCoupon.teaching_course_id, UserCoupon.status,
                              Coupon.money, Coupon.end_time) \
        .join(Coupon, UserCoupon.coupon_id == Coupon.id) \
        .filter(UserCoupon.promo_code == coupon_code, UserCoupon.status > 0, Coupon.status > 0) \
        .first()
    if not coupon:
        data['is_bind'] = True
        return data
    teaching_course = db.session.query(TeachingCourse.course_name, TeachingCourseCouponRelation.id) \
        .join(TeachingCourseCouponRelation, TeachingCourseCouponRelation.teaching_course_id == TeachingCourse.id) \
        .filter(TeachingCourse.id == coupon.teaching_course_id,
                TeachingCourse.organization_id == admin_bind_weixin.organization_id,
                TeachingCourse.status > 0,
                TeachingCourseCouponRelation.coupon_id == coupon.coupon_id,
                TeachingCourseCouponRelation.status > 0) \
        .first()
    if not teaching_course:
        data['is_bind'] = True
        data['is_verify'] = True
        return data
    else:
        data['is_bind'] = True
        data['is_verify'] = True
        data['has_teaching_course'] = True
        if int(coupon.end_time) < int(time.time()):
            data['is_out_of_date'] = True
            return data
        else:
            if coupon.status == 2:
                data['is_used'] = True
                return data
            else:
                db.session.query(UserCoupon).filter(UserCoupon.id == coupon.id) \
                    .update({UserCoupon.status: 2, UserCoupon.bind_weixin_id: admin_bind_weixin.id})
                db.session.commit()
                data['course_name'] = teaching_course.course_name
                data['money'] = coupon.money
                return data
