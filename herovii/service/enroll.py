# -*- coding: utf-8 -*-
import time

from herovii.libs.error_code import DirtyDataError, UpdateDBError
from herovii.libs.helper import get_full_oss_url
from herovii.models.base import db
from herovii.models.org.enroll import Enroll
from herovii.models.org.org_config import OrgConfig
from herovii.models.user.avatar import Avatar

__author__ = 'yangchujie'


def get_stu_enroll_detail_info(blz_id):
    u = db.session.query(Enroll).filter(Enroll.blz_id == blz_id).first()
    if u is not None:
        stu_course = db.session.query(OrgConfig).filter(OrgConfig.id == u.course_id).first()
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == u.student_uid).first()
        stu_avatar_full_path = None
        if stu_avatar:
            stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
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
            'blz_id': u.blz_id,
            'create_time': u.create_time
        }
    else:
        return None
    return data


def update_stu_enroll_info(data):
    res = db.session.query(Enroll).filter(Enroll.blz_id == data['blz_id']).update({Enroll.status: data['status'],
                                                                                   Enroll.confirm_time: time.time()})
    if res:
        data = {
            "status": data['status']
        }
    return data



