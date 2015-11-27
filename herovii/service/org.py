from herovii.libs.error_code import NotFound
from herovii.models.base import db
from herovii.models.org.org_course import OrgCourse
from herovii.models.org.teacher_group import TeacherGroup
from herovii.models.org.teacher_group_realation import TeacherGroupRealation
from herovii.models.org.video import OrgVideo
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
    teachers = db.session.query(UserCSU).filter(UserCSU.uid.in_(l)).all()

    return dto_teachers_group(oid, collection, teachers)


def dto_teachers_group(oid, l, teachers):
    # groups = []
    group_keys = {}
    for t in teachers:
        for uid, group_id, title in l:
            if uid == t.uid:
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
    q = OrgCourse.query.fitler_by(organization_id=oid)
    courses = q.paginate(page, count).items
    total_count = q.count()
    return courses, total_count


def get_course_by_id(cid):
    course = OrgCourse.query.get(cid).first_or_404
    teacher = UserCSU.query.get(course.lecture).first()
    videos = get_video_by_course_id(cid)
    return {
        'course': course,
        'teacher': teacher,
        'videos': videos
    }


def get_video_by_course_id(cid):
    videos = OrgVideo.query.filter_by(course_id=cid).all()
    return videos




