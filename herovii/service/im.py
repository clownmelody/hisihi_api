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
from io import BytesIO
import pycurl
from flask import current_app
from herovii.libs.error_code import ParamException
from herovii.settings import LEAN_CLOUD_X_LC_Id, LEAN_CLOUD_X_LC_Key

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


def create_im_group_service(group_name, member_client_ids, organization_id, conversion_id, group_avatar):
    group = ImGroup(group_name=group_name, create_time=int(time.time()),
                    organization_id=organization_id, conversion_id=conversion_id,
                    group_avatar=group_avatar)
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
    member_list = []
    if not group:
        raise ImGroupNotFound()
    client_id_list = member_client_ids.split(':')
    try:
        for client_id in client_id_list:
            member_list.append(client_id)
            exist_in_group = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                                    ImGroupMember.member_id == client_id) \
                .first()
            if not exist_in_group:
                group_member = ImGroupMember(group_id=group.id, member_id=client_id, create_time=int(time.time()))
                with db.auto_commit():
                    db.session.add(group_member)
    except:
        return False
    # 在 leancloud 中添加群成员
    conversion_id = group.conversion_id
    if conversion_id is None or conversion_id == 0:
        db.session.rollback()
        return False
    code, resp = curl_service_to_lean_cloud("AddUnique", conversion_id, member_list)
    # leancloud 操作异常
    if code//100 != 2:
        db.session.rollback()
        return False
    return True


def delete_im_group_members_service(group_id, member_client_ids):
    group = db.session.query(ImGroup).filter(ImGroup.id == group_id, ImGroup.status == 1).first()
    member_list = []
    if not group:
        raise ImGroupNotFound()
    client_id_list = member_client_ids.split(':')
    try:
        for client_id in client_id_list:
            member_list.append(client_id)
            exist_in_group = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                                    ImGroupMember.member_id == client_id,
                                                                    ImGroupMember.status == 1) \
                .first()
            if exist_in_group:
                db.session.query(ImGroupMember).filter(ImGroupMember.id == exist_in_group.id).update({'status': -1})
    except:
        return False
    # 在 leancloud 中添加群成员
    conversion_id = group.conversion_id
    if conversion_id is None or conversion_id == 0:
        db.session.rollback()
        return False
    code, resp = curl_service_to_lean_cloud("Remove", conversion_id, member_list)
    # leancloud 操作异常
    if code//100 != 2:
        db.session.rollback()
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


# 创建会话
def create_conversion_to_lean_cloud(body_data=None):
    """
    curl -X POST \
      -H "X-LC-Id: tjt1cu4FpyT77H0FzxkQpXlH-gzGzoHsz" \
      -H "X-LC-Key: EJ0aCBygEPMzvoPc61WL6jMf" \
      -H "Content-Type: application/json" \
      -d '{"name":"My Private Room","m": ["BillGates", "SteveJobs"]}' \
      https://api.leancloud.cn/1.1/classes/_Conversation
    """
    if body_data is None:
        raise ParamException()
    head = [
        "X-LC-Id: " + LEAN_CLOUD_X_LC_Id,
        "X-LC-Key: " + LEAN_CLOUD_X_LC_Key,
        "Content-Type: application/json"
    ]
    try:
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://api.leancloud.cn/1.1/classes/_Conversation')
        c.setopt(pycurl.CUSTOMREQUEST, 'POST')
        c.setopt(c.HTTPHEADER, head)
        c.setopt(c.POSTFIELDS, body_data)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        code = c.getinfo(c.HTTP_CODE)
        body = buffer.getvalue()
        c.close()
        return code, body.decode()
    except:
        return 500, None


# 从会话中添加或删除成员
def curl_service_to_lean_cloud(action=None, conversion_id=None, body_data=None):
    """
    curl -X PUT \
      -H "X-LC-Id: tjt1cu4FpyT77H0FzxkQpXlH-gzGzoHsz" \
      -H "X-LC-Key: EJ0aCBygEPMzvoPc61WL6jMf" \
      -H "Content-Type: application/json" \
      -d '{"m": {"__op":"AddUnique","objects":["LarryPage"]}}' \
      https://api.leancloud.cn/1.1/classes/_Conversation/5552c0c6e4b0846760927d5a
    """
    if action is None or conversion_id is None or body_data is None:
        raise ParamException()
    head = [
        "X-LC-Id: " + LEAN_CLOUD_X_LC_Id,
        "X-LC-Key: " + LEAN_CLOUD_X_LC_Key,
        "Content-Type: application/json"
    ]
    body_data = {
        "m": {
            "__op": action,
            "objects": body_data
        }
    }
    body_data = json.dumps(body_data)
    try:
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://api.leancloud.cn/1.1/classes/_Conversation/'+conversion_id)
        c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
        c.setopt(c.HTTPHEADER, head)
        c.setopt(c.POSTFIELDS, body_data)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        code = c.getinfo(c.HTTP_CODE)
        body = buffer.getvalue()
        c.close()
        return code, body.decode()
    except:
        return 500, None