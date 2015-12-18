from _operator import or_, and_
import re
from flask import json
from flask.globals import current_app
from sqlalchemy.sql.expression import text, distinct
from sqlalchemy.sql.functions import func
from werkzeug.datastructures import MultiDict
from herovii.libs.error_code import NotFound, DataArgumentsException, StuClassNotFound
from herovii.libs.helper import get_full_oss_url
from herovii.libs.util import get_today_string, convert_paginate
from herovii.models.base import db
from herovii.models.issue import Issue
from herovii.models.org.class_mirror import ClassMirror
from herovii.models.org.classmate import Classmate
from herovii.models.org.course import Course
from herovii.models.org.enroll import Enroll
from herovii.models.org.info import Info
from herovii.models.org.org_config import OrgConfig
from herovii.models.org.sign_in import StudentSignIn
from herovii.models.org.student_class import StudentClass
from herovii.models.org.teacher_group import TeacherGroup
from herovii.models.org.teacher_group_relation import TeacherGroupRelation
from herovii.models.org.video import Video
from herovii.models.user.avatar import Avatar
from herovii.models.user.user_csu import UserCSU
from herovii.models.user.user_csu_secure import UserCSUSecure

__author__ = 'bliss'


def create_org_info(org):
    with db.auto_commit():
        db.session.add(org)
    return org


def get_org_teachers_by_group(oid):
    # collection = db.session.query(TeacherGroupRelation.uid, TeacherGroupRelation.teacher_group_id,
    #                               TeacherGroup.title).\
    #     outerjoin(TeacherGroup, TeacherGroup.id == TeacherGroupRelation.teacher_group_id).filter(
    #     TeacherGroup.organization_id == oid, TeacherGroup.status != -1, TeacherGroupRelation.status != -1).\
    #     all()

    # relation = aliased
    # 这里需要使用子查询 subquery
    sub_query = db.session.query(TeacherGroupRelation.uid, TeacherGroupRelation.teacher_group_id). \
        filter(TeacherGroupRelation.status != -1).subquery()

    # 需要使用subquery的.c 属性来引用字段
    collection_query = db.session.query(TeacherGroup.id, TeacherGroup.title, sub_query.c.uid). \
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
        join(Avatar, UserCSU.uid == Avatar.uid).filter(UserCSU.uid.in_(l), UserCSU.status != -1). \
        group_by(UserCSU.uid).all()

    return dto_teachers_group_1(oid, collection, teachers)


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
    for group_id, title, uid in l:
        group_keys.add((group_id, title), uid)

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
                if uid == t.uid:
                    avatar = get_full_oss_url(avatar, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
                    t = {'lecture': t, 'avatar': avatar}
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


def get_org_courses_paging(oid, page, count):
    # q = Course.query.filter_by(organization_id=oid)
    # courses = q.paginate(page, count).items
    q = db.session.query(Course, Issue).filter(
        Course.status != -1, Issue.status != -1, Course.organization_id == oid
    ).join(Issue, Course.category_id == Issue.id)
    total_count = q.count()
    start, stop = convert_paginate(page, count)
    courses = q.slice(start, stop).all()
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
    record_total_count = db.session.query(func.count(distinct(StudentSignIn.date))).\
        select_from(StudentSignIn). \
        filter(StudentSignIn.organization_id == oid, text(time_line), StudentSignIn.status != -1).\
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
    blzs_query = db.session.query(
        Enroll, UserCSU.nickname, Course.title,
        Avatar.path
    ).filter(Enroll.organization_id == oid, Enroll.status != -1). \
        join(UserCSU, Enroll.student_uid == UserCSU.uid). \
        join(Avatar, Enroll.student_uid == Avatar.uid). \
        outerjoin(Course, Enroll.course_id == Course.id). \
        order_by(Enroll.create_time.desc())

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
        order_by(Classmate.class_id).all()

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
            UserCSU, get_full_oss_url(Avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')). \
            filter(UserCSU.uid == lid, UserCSU.status != -1). \
            outerjoin(Avatar, UserCSU.uid == Avatar.uid).first()
        return _filter_lecture_dto(lecture)

    mobile = args.get('mobile')
    if mobile:
        lecture = db.session.query(
            UserCSU, get_full_oss_url(Avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')). \
            join(UserCSUSecure, UserCSUSecure.id == UserCSU.uid). \
            filter(UserCSUSecure.mobile == mobile). \
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
        'avatar': avatar
    }
    return json.dumps(data)


def get_org_student_profile_by_uid(uid):
    u = db.session.query(Enroll).filter(Enroll.student_uid == uid).first()
    if u is not None:
        stu_course = db.session.query(OrgConfig).filter(OrgConfig.id == u.course_id).first()
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == uid).first()
        stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        stu_classmate = db.session.query(Classmate).filter(Classmate.uid == uid).first()
        stu_sign_in_count = get_uid_sign_in_total_count_by_now(uid)
        if stu_classmate is None:
            class_group = None
        else:
            class_info = db.session.query(StudentClass).filter(StudentClass.id == stu_classmate.class_id).first()
            if class_info is not None:
                class_group = class_info.title
        if stu_course is None:
            course_name = None
        else:
            course_name = stu_course.value
        data = {
            'uid': u.student_uid,
            'avatar': stu_avatar_full_path,
            'student_name': u.student_name,
            'status': u.status,
            'course_name': course_name,
            'class_group': class_group,
            'sign_in_count': stu_sign_in_count
        }
    else:
        return None
    return data


def get_org_student_sign_in_history_by_uid(uid, page, per_page):
    start = (page - 1) * per_page
    stop = start + per_page
    student_class = db.session.query(Classmate).filter(Classmate.uid == uid, Classmate.status == 1).first()
    if student_class is None:
        raise StuClassNotFound
    class_mirror_total_count = db.session.query(ClassMirror).filter(ClassMirror.class_id == student_class.class_id).count()
    class_mirror_list = db.session.query(ClassMirror).filter(ClassMirror.class_id == student_class.class_id)\
        .slice(start, stop)\
        .all()
    if class_mirror_list is None:
        return None
    sign_in_dto = []
    for class_mirror in class_mirror_list:
        sign_in = db.session.query(StudentSignIn.uid, StudentSignIn.organization_id, StudentSignIn.date) \
            .filter(StudentSignIn.uid == uid, StudentSignIn.status != -1, StudentSignIn.date == class_mirror.date)\
            .order_by(StudentSignIn.sign_in_time.desc()) \
            .first()
        if sign_in is not None:
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
    return class_mirror_total_count, sign_in_dto


def get_class_sign_in_detail_by_date(oid, cid, date, page, per_page):
    exist_class_in_org = db.session.query(StudentClass).filter(StudentClass.organization_id == oid,
                                                               StudentClass.status == 1,
                                                               StudentClass.id == cid).first()
    if exist_class_in_org:
        start = (page - 1) * per_page
        stop = start + per_page
        total_count = db.session.query(Classmate.uid). \
            filter(Classmate.status == 1, Classmate.class_id == cid). \
            order_by(Classmate.uid.desc()). \
            count()
        stu_list = db.session.query(Classmate.uid). \
            filter(Classmate.status == 1, Classmate.class_id == cid). \
            order_by(Classmate.uid.desc()). \
            slice(start, stop).all()
        data_list = []
        for stu in stu_list:
            exist_sign_in = db.session.query(StudentSignIn.id).filter(StudentSignIn.organization_id == oid,
                                                                      StudentSignIn.status == 1,
                                                                      StudentSignIn.uid == stu.uid,
                                                                      StudentSignIn.date == date).first()
            user_info = db.session.query(UserCSU).filter(UserCSU.uid == stu.uid).first()
            stu_avatar = db.session.query(Avatar).filter(Avatar.uid == stu.uid).first()
            stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
            user = {"uid": stu.uid, 'avatar': stu_avatar_full_path, 'nickname': user_info.nickname}
            if exist_sign_in:
                user['sign_in_status'] = True
            else:
                user['sign_in_status'] = False
            data_list.append(user)
    else:
        raise DataArgumentsException()
    return data_list, total_count


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
