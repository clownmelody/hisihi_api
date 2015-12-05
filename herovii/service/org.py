from _operator import or_
from flask import jsonify
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import func
from herovii.libs.error_code import NotFound
from herovii.libs.helper import get_full_oss_url
from herovii.models.base import db
from herovii.models.org import enroll
from herovii.models.org.course import Course
from herovii.models.org.enroll import Enroll
from herovii.models.org.info import Info
from herovii.models.org.sign_in import StudentSignIn
from herovii.models.org.teacher_group import TeacherGroup
from herovii.models.org.teacher_group_realation import TeacherGroupRealation
from herovii.models.org.video import Video
from herovii.models.user.avatar import Avatar
from herovii.models.user.user_csu import UserCSU

__author__ = 'bliss'


def create_org_info(org):
    with db.auto_commit():
        db.session.add(org)
    return org


def get_org_teachers_by_group(oid):

    collection = db.session.query(TeacherGroupRealation.uid, TeacherGroupRealation.teacher_group_id,
                                  TeacherGroup.title).\
        join(TeacherGroup, TeacherGroup.id == TeacherGroupRealation.teacher_group_id).filter_by(
        organization_id=oid).all()

    m = map(lambda x: x[0], collection)
    l = list(m)
    teachers = db.session.query(UserCSU, Avatar.path). \
        join(Avatar, UserCSU.uid == Avatar.uid).filter(UserCSU.uid.in_(l)).all()

    return dto_teachers_group(oid, collection, teachers)


def dto_teachers_group(oid, l, teachers):
    # groups = []
    group_keys = {}
    for t, avatar in teachers:
        avatar = get_full_oss_url(avatar, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        t = {'teacher': t, 'avatar': avatar}
        for uid, group_id, title in l:
            if uid == t['teacher'].uid:
                if group_keys.get(group_id):
                    group_keys[group_id]['teachers'].append(t)
                    # group_keys.append(group_id)

                else:
                    group = {
                        'group_id': group_id,
                        'group_title': title,
                        'teachers': [t]
                    }
                    group_keys[group_id] = group

    groups = tuple(group_keys.values())

    return {
        'org_id': oid,
        'groups': groups
    }


def dto_org_courses_paginate(oid, page, count):
    courses, total_count = get_org_courses_paging(oid, page, count)
    if not courses:
        raise NotFound(error='courses not found')
    m = map(lambda x: x.lecture, courses)
    l = list(m)
    teachers = UserCSU.query.filter(UserCSU.id_in(l)).all()
    c_l = []
    for c in courses:
        course = {
                'course': c,
            }

        for t in teachers:
            if t.id == c.lecture:
                course['teacher'] = t
        c_l.append(course)
    return {
        'organization_id': oid,
        'total_count': total_count,
        'courses': c_l
    }


def get_org_courses_paging(oid, page ,count):
    q = Course.query.fitler_by(organization_id=oid)
    courses = q.paginate(page, count).items
    total_count = q.count()
    return courses, total_count


def get_course_by_id(cid):
    course = Course.query.get(cid).first_or_404
    teacher = UserCSU.query.get(course.lecture).first()
    videos = get_video_by_course_id(cid)
    return {
        'course': course,
        'teacher': teacher,
        'videos': videos
    }


def get_video_by_course_id(cid):
    videos = Video.query.filter_by(course_id=cid).all()
    return videos


def create_org_pics(pics):
    print(pics)
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
    counts = db.session.query(func.count('*')).\
        filter(Enroll.organization_id == oid).\
        group_by(Enroll.status).\
        having(or_(Enroll.status == 1, Enroll.status == 2)).\
        all()
    return counts


def view_sign_in_count(oid, form):
    since = form.since.data
    end = form.end.data
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    start = (page-1) * per_page
    stop = start+per_page
    time_line = ''
    if since and end:
        time_line = 'create_time >=' + since + 'and create_time <=' + end
    if since and not end:
        time_line = 'create_time >=' + since
    if not since and end:
        time_line = 'create_time <=' + end
    counts = db.session.query(func.count('*')).\
        filter(StudentSignIn.organization_id == oid, text(time_line)).\
        group_by(StudentSignIn.date).\
        slice(start, stop)
    total = db.session.query().select_from(Enroll).filter_by(status=2).count()
    return counts, total


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


def dto_get_blzs_paginate(page, count, oid):
    # 可能会造成性能低下，尽量将筛选条件在第一次join时应用，以减少记录数
    # query里用到outerjoin是因为不希望在course为null的情况下造成没有查询结果
    # 使用outerjoin将保证即使没有课程，也可以筛选报名结果
    blzs_query = db.session.query(
        Enroll, UserCSU.nickname, Course.title,
        get_full_oss_url(Avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
    ).filter(Enroll.organization_id == oid).\
        join(UserCSU, Enroll.student_uid == UserCSU.uid).\
        join(Avatar, Enroll.student_uid == Avatar.uid).\
        outerjoin(Course, Enroll.course_id == Course.id).\
        order_by(Enroll.create_time.desc())

    blzs_query = blzs_query.offset((page-1) * count)
    blzs_query = blzs_query.limit(count)
    blzs = blzs_query.all()
    dto_blzs = __assign_blzs(blzs)
    return dto_blzs


def __assign_blzs(blzs):
    dto_blz = []
    for blz in blzs:
        # for blz_base, nickname, avatar in blz:
        data = {
            'blz': blz[0],
            'name': blz[1],
            'course': blz[2],
            'avatar': blz[3]
        }
        dto_blz.append(data)
    return dto_blz

