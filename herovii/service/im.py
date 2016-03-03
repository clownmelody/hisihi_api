# -*- coding: utf-8 -*-
import hmac, hashlib
import json
from random import Random
import time
from flask import current_app
from herovii import db
from herovii.libs.error_code import ImGroupNotFound, ServerError, NotFound, PushToClassFailture, IllegalOperation, \
    CreateImGroupFailture
from herovii.libs.helper import get_full_oss_url
from herovii.libs.lean_cloud_system_message import LeanCloudSystemMessage
from herovii.models import OrgAdmin
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
from herovii.libs.error_code import ParamException
from herovii.secure import LEAN_CLOUD_X_LC_Id, LEAN_CLOUD_X_LC_Key

__author__ = 'yangchujie'


# LeanCloud 签名算法
def sign(msg, k):
    return hmac.new(bytes(k, 'utf-8'), bytes(msg, 'utf-8'), hashlib.sha1).hexdigest()


# 获取当前时间戳
def get_timestamp():
    return int(time.time())


# 生成随机字符串
def get_nonce(nonce_length=8):
    nonce = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(nonce_length):
        nonce += chars[random.randint(0, length)]
    return nonce


def create_im_group_service(group_name, member_client_ids, organization_id, conversation_id, group_avatar, admin_uid,
                            description):
    if member_client_ids is None:
        client_id_list = [admin_uid]
    else:
        client_id_list = member_client_ids.split(':')
        client_id_list.append(admin_uid)
    group = ImGroup(group_name=group_name, create_time=int(time.time()),
                    organization_id=organization_id, conversation_id=conversation_id,
                    group_avatar=group_avatar, description=description)
    with db.auto_commit():
        try:
            db.session.add(group)
            db.session.commit()
        except:
            return 0, False
        for client_id in client_id_list:
            group_member = ImGroupMember(group_id=group.id, member_id=client_id, create_time=int(time.time()))
            with db.auto_commit():
                db.session.add(group_member)
    update_im_group_admin_uid(group.id, admin_uid)  # 修改群管理员
    # 未传入会话id
    if conversation_id == 0:
        body = {
            "name": group_name,
            "m": client_id_list,
            "attr": {
                "type": "group",
                "group_id": group.id
            }
        }
        code, res = create_conversation_to_lean_cloud(json.dumps(body))
        if code != 201:
            raise CreateImGroupFailture()
        res = json.loads(res)
        conversation_id = res['objectId']
        db.session.query(ImGroup).filter(ImGroup.id == group.id).update({'conversation_id': conversation_id})
    # 发送系统通知
    LeanCloudSystemMessage.push_added_to_group_message(admin_uid, group.id, client_id_list)
    return group.id, conversation_id, True


def update_im_group_service(group_id, group_name):
    try:
        db.session.query(ImGroup).filter(ImGroup.id == group_id).update({'group_name': group_name})
    except:
        return False
    # 发送系统通知
    LeanCloudSystemMessage.push_group_info_been_modified_message(0, group_id, group_name)
    return True


def delete_im_group_service(group_id):
    try:
        db.session.query(ImGroup).filter(ImGroup.id == group_id).update({'status': -1})
    except:
        return False
    # 发送系统通知
    LeanCloudSystemMessage.push_admin_dismiss_group_message(0, group_id)
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
        # 发送系统通知
        LeanCloudSystemMessage.push_admin_dismiss_group_message(uid, group_id)
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
                if is_group_available_to_add_member(group.id):  # 群成员数量未达到上限
                    group_member = ImGroupMember(group_id=group.id, member_id=client_id, create_time=int(time.time()))
                    db.session.add(group_member)
            else:
                if exist_in_group.status == '-1':
                    db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                           ImGroupMember.member_id == client_id)\
                        .update({'status': 1})
    except:
        return False
    # 在 leancloud 中添加群成员
    conversation_id = group.conversation_id
    if conversation_id is None or conversation_id == 0:
        db.session.rollback()
        return False
    code, resp = curl_service_to_lean_cloud("AddUnique", conversation_id, member_list)
    # leancloud 操作异常
    if code // 100 != 2:
        db.session.rollback()
        return False
    db.session.commit()
    # 发送系统通知
    LeanCloudSystemMessage.push_added_to_group_message(0, group_id, client_id_list)
    return True


# 检查群组成员是否已达上限
def is_group_available_to_add_member(group_id=None):
    group = db.session.query(ImGroup).filter(ImGroup.id == group_id, ImGroup.status == 1).first()
    if group:
        member_count = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                              ImGroupMember.status == 1) \
            .count()
        if group.level > member_count:
            return True
        else:
            return False
    else:
        raise ImGroupNotFound()


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
    # 在 leancloud 中删除群成员
    conversation_id = group.conversation_id
    if conversation_id is None or conversation_id == 0:
        db.session.rollback()
        return False
    code, resp = curl_service_to_lean_cloud("Remove", conversation_id, member_list)
    # leancloud 操作异常
    if code // 100 != 2:
        db.session.rollback()
        return False
    # 发送系统通知
    LeanCloudSystemMessage.push_removed_from_group_message(admin_member.member_id, group_id, client_id_list)
    return True


def get_organization_im_groups_service(organization_id, page, per_page):
    start = (page - 1) * per_page
    stop = start + per_page
    group_total_count = db.session.query(ImGroup).filter(
        ImGroup.organization_id == organization_id,
        ImGroup.status == 1) \
        .count()
    group_list = db.session.query(ImGroup).filter(
        ImGroup.organization_id == organization_id,
        ImGroup.status == 1) \
        .slice(start, stop) \
        .all()
    result_list = []
    for group in group_list:
        g = {
            "id": group.id,
            "group_name": group.group_name,
            "group_avatar": group.group_avatar,
            "description": group.description,
            "create_time": group.create_time,
            "level": group.level,
            "conversation_id": group.conversation_id
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
def create_conversation_to_lean_cloud(body_data=None):
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
def curl_service_to_lean_cloud(action=None, conversation_id=None, body_data=None):
    """
    curl -X PUT \
      -H "X-LC-Id: tjt1cu4FpyT77H0FzxkQpXlH-gzGzoHsz" \
      -H "X-LC-Key: EJ0aCBygEPMzvoPc61WL6jMf" \
      -H "Content-Type: application/json" \
      -d '{"m": {"__op":"AddUnique","objects":["LarryPage"]}}' \
      https://api.leancloud.cn/1.1/classes/_Conversation/5552c0c6e4b0846760927d5a
    """
    if action is None or conversation_id is None or body_data is None:
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
        c.setopt(c.URL, 'https://api.leancloud.cn/1.1/classes/_Conversation/' + conversation_id)
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


# 根据 client_id 获取用户基本信息
def get_user_profile_by_client_id(client_id=None):
    if client_id is None:
        return None
    if client_id.startswith('c'):  # 普通用户
        length = len(client_id)
        uid = client_id[1:length]
        user = db.session.query(UserCSU).filter(UserCSU.uid == uid).first()
    elif client_id.startswith('o'):  # 机构管理员
        length = len(client_id)
        uid = client_id[1:length]
        user = db.session.query(OrgAdmin).filter(OrgAdmin.id == uid).first()
    else:
        uid = client_id
        user = db.session.query(UserCSU).filter(UserCSU.uid == uid).first()
    if user:
        avatar = db.session.query(Avatar).filter(Avatar.uid == uid).first()
        if avatar:
            avatar_full_path = get_full_oss_url(avatar.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
        else:
            avatar_full_path = None
        if hasattr(user, 'nickname'):
            nickname = user.nickname
        else:
            nickname = user.username
        user_detail = {
            'client_id': client_id,
            'nickname': nickname,
            'avatar': avatar_full_path
        }
        return user_detail
    else:
        return None


# 根据 group_id 获取群信息
def get_group_info_by_group_id(group_id=None):
    if group_id is None:
        return None
    group = db.session.query(ImGroup).filter(
        ImGroup.id == group_id, ImGroup.status == 1).first()
    if group:
        group = {
            "id": group.id,
            "group_name": group.group_name,
            "organization_id": group.organization_id,
            "conversation_id": group.conversation_id,
            "group_avatar": group.group_avatar,
            "description": group.description,
            "create_time": group.create_time,
            "level": group.level
        }
        return group
    else:
        raise ImGroupNotFound()


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


# 根据 group_id 获取所有群成员的 client_ids 列表
def get_group_member_client_ids_by_group_id(group_id=None):
    client_id_list = []
    if group_id is None:
        return None
    group_member_list = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                               ImGroupMember.status == 1).all()
    if group_member_list:
        for group_member in group_member_list:
            member_client_id = group_member.member_id
            client_id_list.append(member_client_id)
    else:
        return None
    return client_id_list


# 修改群组的管理员
def update_im_group_admin_uid(group_id=None, admin_uid=None):
    exist_in_group = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                            ImGroupMember.member_id == admin_uid,
                                                            ImGroupMember.status == 1).count()
    if exist_in_group:
        db.session.query(ImGroupMember).filter(ImGroupMember.member_id == admin_uid).update({'is_admin': 1})
    else:
        group_member = ImGroupMember(group_id=group_id, member_id=admin_uid, create_time=int(time.time()), is_admin=1)
        with db.auto_commit():
            db.session.add(group_member)


# 获取用户的所有群组
def get_im_user_groups_service(client_id=None):
    group_member_list = db.session.query(ImGroupMember).filter(ImGroupMember.member_id == client_id,
                                                               ImGroupMember.status == 1).all()
    group_info_list = []
    for group_member in group_member_list:
        group_id = group_member.group_id
        group_info = get_group_info_by_group_id(group_id)
        group_info_list.append(group_info)
    return group_info_list


# 获取群组详情(包括群组信息和群成员的信息)
def get_im_group_detail_service(group_id):
    group = get_group_info_by_group_id(group_id)
    if group:
        # 获取群成员和群主
        group_member_list = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                                   ImGroupMember.status == 1).all()
        member_info_list = []
        for group_member in group_member_list:
            user_detail = get_user_profile_by_client_id(group_member.member_id)
            if user_detail:
                user_detail['is_admin'] = group_member.is_admin
                member_info_list.append(user_detail)
        group_detail = {
            "group_info": group,
            "group_member_info": member_info_list
        }
        return group_detail
    else:
        return None


# 根据群组id获取群管理员信息
def get_group_admin_member_by_group_id(group_id):
    group_admin = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                         ImGroupMember.is_admin == 1,
                                                         ImGroupMember.status == 1).first()
    if group_admin:
        result_array = [group_admin.member_id]
        return result_array
    else:
        return None


# 检查 client_id 是否是群成员
def is_client_id_in_group_member(group_id, client_id):
    is_exist = db.session.query(ImGroupMember).filter(ImGroupMember.group_id == group_id,
                                                      ImGroupMember.member_id == client_id,
                                                      ImGroupMember.status == 1).count()
    if is_exist:
        return True
    return False
