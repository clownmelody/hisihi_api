# -*- coding: utf-8 -*-
import hmac, hashlib
import json
from random import Random
import time
from herovii import db
from herovii.libs.error_code import ImGroupNotFound
from herovii.libs.helper import get_full_oss_url
from herovii.models.im.im_group import ImGroup
from herovii.models.im.im_group_member import ImGroupMember
from herovii.models.org.classmate import Classmate
from herovii.models.org.student_class import StudentClass
from herovii.models.org.teacher_group_relation import TeacherGroupRelation
from herovii.models.user.avatar import Avatar
from herovii.models.user.user_csu import UserCSU

__author__ = 'yangchujie'


# LeanCloud 签名算法
def sign(msg, k):
    return hmac.new(bytes(k, 'utf-8'), bytes(msg, 'utf-8'), hashlib.sha1).hexdigest()


# 获取当前时间戳
def get_timestamp():
    return str(time.time())


# 生成随机字符串
def get_nonce(nonce_length=8):
    nonce = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(nonce_length):
        nonce += chars[random.randint(0, length)]
    return nonce


def create_im_group_service(group_name, member_client_ids):
    group = ImGroup(group_name=group_name, create_time=int(time.time()))
    with db.auto_commit():
        try:
            db.session.add(group)
            db.session.commit()
        except:
            return 0, False
        client_id_list = member_client_ids.split(':')
        for client_id in client_id_list:
            group_member = ImGroupMember(group_id=group.id, member_id=client_id, create_time=int(time.time()))
            with db.auto_commit():
                db.session.add(group_member)
    return group.id, True


def update_im_group_service(group_id, group_name):
    try:
        db.session.query(ImGroup).filter(ImGroup.id == group_id).update({'group_name': group_name})
    except:
        return False
    return True


def delete_im_group_service(group_id):
    try:
        db.session.query(ImGroup).filter(ImGroup.id == group_id).update({'status': -1})
    except:
        return False
    return True


def add_im_group_members_service(group_id, member_client_ids):
    group = db.session.query(ImGroup).filter(ImGroup.id == group_id, ImGroup.status == 1).first()
    if not group:
        raise ImGroupNotFound()
    client_id_list = member_client_ids.split(':')
    try:
        for client_id in client_id_list:
            exist_in_group = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                                    ImGroupMember.member_id == client_id) \
                .first()
            if not exist_in_group:
                group_member = ImGroupMember(group_id=group.id, member_id=client_id, create_time=int(time.time()))
                with db.auto_commit():
                    db.session.add(group_member)
    except:
        return False
    return True


def delete_im_group_members_service(group_id, member_client_ids):
    group = db.session.query(ImGroup).filter(ImGroup.id == group_id, ImGroup.status == 1).first()
    if not group:
        raise ImGroupNotFound()
    client_id_list = member_client_ids.split(':')
    try:
        for client_id in client_id_list:
            exist_in_group = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                                    ImGroupMember.member_id == client_id,
                                                                    ImGroupMember.status == 1) \
                .first()
            if exist_in_group:
                db.session.query(ImGroupMember).filter(ImGroupMember.id == exist_in_group.id).update({'status': -1})
    except:
        return False
    return True


def get_organization_im_groups_service(organization_id, page, per_page):
    start = (page - 1) * per_page
    stop = start + per_page
    group_total_count = db.session.query(ImGroup).filter(
        ImGroup.organization_id == organization_id,
        ImGroup.status == 1) \
        .count()
    group_list = db.session.query(ImGroup.id, ImGroup.group_name).filter(
        ImGroup.organization_id == organization_id,
        ImGroup.status == 1) \
        .slice(start, stop) \
        .all()
    result_list = []
    for group in group_list:
        g = {
            "id": group.id,
            "group_name": group.group_name
        }
        result_list.append(g)
    return group_total_count, result_list


def get_organization_im_contacts_service(organization_id):
    group_list = db.session.query(ImGroup.id, ImGroup.group_name, ImGroup.group_avatar).filter(
        ImGroup.organization_id == organization_id,
        ImGroup.status == 1) \
        .all()
    result_list = []
    for group in group_list:
        g = {
            "id": group.id,
            "name": group.group_name,
            "avatar": group.group_avatar,
            "type": "group"
        }
        result_list.append(g)
    teacher_list = db.session.query(TeacherGroupRelation).filter(TeacherGroupRelation.group == 6,
                                                                 TeacherGroupRelation.status == 1,
                                                                 TeacherGroupRelation.organization_id == organization_id)\
        .all()
    for teacher in teacher_list:
        uid = teacher.uid
        user = db.session.query(UserCSU).filter(UserCSU.uid == uid).first()
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == uid).first()
        stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        tea_object = {
            "id": teacher.uid,
            "name": user.nickname,
            "avatar": stu_avatar_full_path,
            "type": "user"
        }
        result_list.append(tea_object)
    student_list = db.session.query(Classmate.uid).join(StudentClass, Classmate.class_id == StudentClass.id)\
        .filter(StudentClass.organization_id == organization_id, StudentClass.status == 1, Classmate.status != -1)\
        .all()
    for student in student_list:
        user = db.session.query(UserCSU).filter(UserCSU.uid == student.uid).first()
        stu_avatar = db.session.query(Avatar).filter(Avatar.uid == student.uid).first()
        if stu_avatar:
            stu_avatar_full_path = get_full_oss_url(stu_avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        tea_object = {
            "id": teacher.uid,
            "name": user.nickname,
            "avatar": stu_avatar_full_path,
            "type": "user"
        }
        result_list.append(tea_object)
    return result_list
