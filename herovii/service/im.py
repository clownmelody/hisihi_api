# -*- coding: utf-8 -*-
import hmac, hashlib
import json
from random import Random
import time
from herovii import db
from herovii.libs.error_code import ImGroupNotFound, ServerError, NotFound, PushToClassFailture, IllegalOperation
from herovii.libs.helper import get_full_oss_url
from herovii.models.im.im_group import ImGroup
from herovii.models.im.im_group_member import ImGroupMember
from herovii.models.org.class_push_history import ClassPushHistory
from herovii.models.org.classmate import Classmate
from herovii.models.org.student_class import StudentClass
from herovii.models.org.teacher_group_relation import TeacherGroupRelation
from herovii.models.user.avatar import Avatar
from herovii.models.user.user_csu import UserCSU
from io import BytesIO
import pycurl
from flask import current_app
from herovii.libs.error_code import ParamException

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


def create_im_group_service(group_name, member_client_ids, organization_id, conversion_id, group_avatar, admin_uid):
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
    update_im_group_admin_uid(group.id, admin_uid)  # 修改群管理员
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


def dismiss_im_group_service(uid, group_id):
    is_group_admin = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                            ImGroupMember.member_id == uid,
                                                            ImGroupMember.is_admin == 1,
                                                            ImGroupMember.status == 1)
    if is_group_admin:
        try:
            db.session.query(ImGroup).filter(ImGroup.id == group_id).update({'status': -1})
        except:
            return False
        return True
    else:
        raise IllegalOperation(error='you are not the administrator of the group')


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
    if code // 100 != 2:
        db.session.rollback()
        return False
    return True


def delete_im_group_members_service(group_id, member_client_ids):
    group = db.session.query(ImGroup).filter(ImGroup.id == group_id, ImGroup.status == 1).first()
    member_list = []
    if not group:
        raise ImGroupNotFound()
    client_id_list = member_client_ids.split(':')
    # 检查待删除成员中是否包含该群组管理员
    admin_member = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                          ImGroupMember.is_admin == 1,
                                                          ImGroupMember.status == 1) \
        .first()
    if admin_member.member_id in client_id_list:
        raise IllegalOperation(error='the member list you want delete contains the administrator of the group')
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
    if code // 100 != 2:
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
                                                                 TeacherGroupRelation.organization_id == organization_id) \
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
    student_list = db.session.query(Classmate.uid).join(StudentClass, Classmate.class_id == StudentClass.id) \
        .filter(StudentClass.organization_id == organization_id, StudentClass.status == 1, Classmate.status != -1) \
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
        "X-LC-Id: " + current_app.config['LEAN_CLOUD_X_LC_Id'],
        "X-LC-Key: " + current_app.config['LEAN_CLOUD_X_LC_Key'],
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
        "X-LC-Id: " + current_app.config['LEAN_CLOUD_X_LC_Id'],
        "X-LC-Key: " + current_app.config['LEAN_CLOUD_X_LC_Key'],
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
        c.setopt(c.URL, 'https://api.leancloud.cn/1.1/classes/_Conversation/' + conversion_id)
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


# 向班级所有学生发送消息通知
def push_message_to_all_classmates_service(class_id):
    # 检查班级是否有效
    if check_is_class_id_valid(class_id):
        # if check_is_enable_to_push(class_id):
        #     send_im_message()
        # else:
        if not check_is_enable_to_push(class_id):
            raise PushToClassFailture()
        return mark_class_push_message_history(class_id)
    else:
        raise NotFound()


# 发送 IM 消息
def send_im_message(from_client_id, to_client_id, message):
    pass


# 标记班级群发消息历史
def mark_class_push_message_history(class_id):
    class_push_history = ClassPushHistory(class_id=class_id)
    with db.auto_commit():
        try:
            db.session.add(class_push_history)
            db.session.commit()
        except:
            raise ServerError()
        return class_push_history.id


# 检查班级id是否有效
def check_is_class_id_valid(class_id):
    try:
        count = db.session.query(StudentClass).filter(
            StudentClass.id == class_id,
            StudentClass.status == 1) \
            .count()
    except:
        raise ServerError()
    return count


# 检查当天是否已经推送过
def check_is_enable_to_push(class_id):
    count = db.session.query(ClassPushHistory).filter(
        ClassPushHistory.class_id == class_id,
        ClassPushHistory.date == time.strftime('%Y-%m-%d', time.localtime(time.time())),
        ClassPushHistory.status == 1) \
        .count()
    return not count


# 根据 client_id 获取用户 reg_id
def get_reg_id_by_client_id(client_id=None):
    if client_id is None:
        return None
    if client_id.startswith('c'):  # 普通用户
        length = len(client_id)
        uid = client_id[1:length]
    elif client_id.startswith('o'):
        return None
    else:
        uid = client_id
    user = db.session.query(UserCSU).filter(UserCSU.uid == uid).first()
    if user:
        return user.reg_id
    else:
        return None


# 根据 group_id 获取群信息
def get_group_info_by_group_id(group_id=None):
    if group_id is None:
        return None
    group = db.session.query(ImGroup).filter(
        ImGroup.id == group_id, ImGroup.status == 1).first()
    return group


# 根据 group_id 获取所有群成员的 reg_id 列表
def get_group_member_reg_ids_by_group_id(group_id=None):
    reg_id_list = []
    if group_id is None:
        return None
    group_member_list = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                               ImGroupMember.status == 1).all()
    if group_member_list:
        for group_member in group_member_list:
            member_uid = group_member.member_id
            if member_uid.startswith('c') or member_uid.startswith('o'):
                length = len(member_uid)
                member_uid = member_uid[1:length]
            else:
                member_uid = member_uid
            reg_id = get_reg_id_by_client_id(member_uid)
            if reg_id:
                reg_id_list.append(reg_id)
    else:
        return None
    return reg_id_list


# 修改群组的管理员
def update_im_group_admin_uid(group_id=None, admin_uid=None):
    exist_in_group = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                            ImGroupMember.member_id == admin_uid,
                                                            ImGroupMember.status == 1)
    if exist_in_group:
        db.session.query(ImGroupMember).filter(ImGroupMember.id == exist_in_group.id).update({'is_admin': 1})
    else:
        group_member = ImGroupMember(group_id=group_id, member_id=admin_uid, create_time=int(time.time()), is_admin=1)
        with db.auto_commit():
            db.session.add(group_member)
