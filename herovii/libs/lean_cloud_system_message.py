# -*- coding: utf-8 -*-
import json
import pycurl
from io import BytesIO
from herovii.libs.error_code import ParamException, SendSysMessageFailture
from herovii.secure import LEAN_CLOUD_X_LC_Id, LEAN_CLOUD_X_LC_Key, LEAN_CLOUD_SYSTEM_CONVERSATION_ID, \
    LEAN_CLOUD_X_LC_Key_SYS

__author__ = 'yangchujie'

"""
IM 业务中的通知服务(采用 leancloud 的系统消息)
"""


class LeanCloudSystemMessage(object):
    @staticmethod
    def push_removed_from_group_message(uid=None, gid=None, member_client_ids=None):
        """
        成员被移除群聊，向所有群成员发系统消息
        """
        from herovii.service.im import get_group_admin_member_by_group_id, get_user_profile_by_client_id, \
            get_group_info_by_group_id
        nickname_list = []
        for client_id in member_client_ids:
            user_detail = get_user_profile_by_client_id(client_id)
            if user_detail:
                nickname_list.append(user_detail['nickname'])
        nickname_list_str = "、".join(nickname_list)
        # all_group_members = get_group_member_client_ids_by_group_id(gid)
        group_admin_user = get_group_admin_member_by_group_id(gid)
        group = get_group_info_by_group_id(gid)
        message_text = "已退出 " + group['group_name'] + " 群"
        message_content = {
            "_lctype": 1,
            "_lctext": message_text,
            "_lcattrs": {
                "message_info": message_text,
                "sys_message_type": "removed_from_group",
                "uid": member_client_ids[0],
                "gid": gid,
                "type": "group",
                "username": nickname_list_str,
                "group_name": group['group_name'],
                "conversation_id": group['conversation_id'],
                "member_client_ids": member_client_ids
            }
        }
        message_content = json.dumps(message_content)
        body_data = {
            "from_peer": member_client_ids[0],
            "message": message_content,
            "to_peers": group_admin_user,
            "conv_id": LEAN_CLOUD_SYSTEM_CONVERSATION_ID,
            "transient": False,
            "no_sync": True
        }
        body_data = json.dumps(body_data)
        return LeanCloudSystemMessage.send_system_message(body_data)

    @staticmethod
    def push_added_to_group_message(uid=None, gid=None, member_client_ids=None):
        """
        成员被添加到群聊，向所有群成员发系统消息
        """
        from herovii.service.im import get_user_profile_by_client_id, get_group_info_by_group_id, \
            get_group_member_client_ids_by_group_id
        nickname_list = []
        for client_id in member_client_ids:
            user_detail = get_user_profile_by_client_id(client_id)
            if user_detail:
                nickname_list.append(user_detail['nickname'])
        nickname_list_str = "、".join(nickname_list)
        all_group_members = get_group_member_client_ids_by_group_id(gid)
        message_text = nickname_list_str + " 加入群聊"
        group = get_group_info_by_group_id(gid)
        message_content = {
            "_lctype": 1,
            "_lctext": message_text,
            "_lcattrs": {
                "message_info": message_text,
                "sys_message_type": "added_to_group",
                "uid": uid,
                "gid": gid,
                "type": "group",
                "username": nickname_list_str,
                "group_name": group['group_name'],
                "conversation_id": group['conversation_id'],
                "member_client_ids": member_client_ids
            }
        }
        message_content = json.dumps(message_content)
        body_data = {
            "from_peer": uid,
            "message": message_content,
            "to_peers": all_group_members,
            "conv_id": LEAN_CLOUD_SYSTEM_CONVERSATION_ID,
            "transient": False,
            "no_sync": True
        }
        body_data = json.dumps(body_data)
        return LeanCloudSystemMessage.send_system_message(body_data)

    @staticmethod
    def push_group_info_been_modified_message(uid=None, gid=None, group_name=None):
        """
        群组基本信息被修改，向所有群成员发系统消息
        """
        from herovii.service.im import get_group_member_client_ids_by_group_id, get_group_info_by_group_id
        all_group_members = get_group_member_client_ids_by_group_id(gid)
        message_text = "XXX 修改了群名称为：" + group_name
        group = get_group_info_by_group_id(gid)
        message_content = {
            "_lctype": 1,
            "_lctext": message_text,
            "_lcattrs": {
                "message_info": message_text,
                "sys_message_type": "group_info_been_modified",
                "uid": uid,
                "gid": gid,
                "group_name": group['group_name'],
                "type": "group",
                "conversation_id": group['conversation_id']
            }
        }
        message_content = json.dumps(message_content)
        body_data = {
            "from_peer": uid,
            "message": message_content,
            "to_peers": all_group_members,
            "conv_id": LEAN_CLOUD_SYSTEM_CONVERSATION_ID,
            "transient": False,
            "no_sync": True
        }
        body_data = json.dumps(body_data)
        return LeanCloudSystemMessage.send_system_message(body_data)

    @staticmethod
    def push_admin_dismiss_group_message(uid=None, gid=None):
        """
        群组被群管理员解散，向所有群成员发系统消息
        """
        from herovii.service.im import get_group_info_by_group_id, get_group_member_client_ids_by_group_id
        all_group_members = get_group_member_client_ids_by_group_id(gid)
        group = get_group_info_by_group_id(gid)
        message_text = "你被移出群聊：" + group['group_name']
        message_content = {
            "_lctype": 1,
            "_lctext": message_text,
            "_lcattrs": {
                "message_info": message_text,
                "sys_message_type": "group_been_dismissed",
                "uid": uid,
                "gid": gid,
                "type": "group",
                "group_name": group['group_name'],
                "conversation_id": group['conversation_id']
            }
        }
        message_content = json.dumps(message_content)
        body_data = {
            "from_peer": "嘿设汇管理员",
            "message": message_content,
            "to_peers": all_group_members,
            "conv_id": LEAN_CLOUD_SYSTEM_CONVERSATION_ID,
            "transient": False,
            "no_sync": True
        }
        body_data = json.dumps(body_data)
        return LeanCloudSystemMessage.send_system_message(body_data)

    @staticmethod
    def push_user_join_in_group_apply_message(uid=None, gid=None):
        """
        用户加群申请的消息
        """
        from herovii.service.im import get_group_admin_member_by_group_id
        from herovii.service.im import get_user_profile_by_client_id
        from herovii.service.im import get_group_info_by_group_id
        group_admin_user = get_group_admin_member_by_group_id(gid)
        user_detail = get_user_profile_by_client_id(uid)
        group = get_group_info_by_group_id(gid)
        message_text = "申请加入 " + group['group_name'] + " 群"
        # if user_detail:
        #     nickname = user_detail['nickname']
        #     message_text = nickname + " 申请加入 "+ group['group_name'] +" 群"
        # else:
        #     message_text = uid + " 申请加入该群"
        message_content = {
            "_lctype": 1,
            "_lctext": message_text,
            "_lcattrs": {
                "message_info": message_text,
                "sys_message_type": "user_join_group_apply",
                "uid": uid,
                "gid": gid,
                "type": "group",
                "username": user_detail['nickname'],
                "group_name": group['group_name'],
                "conversation_id": group['conversation_id']
            }
        }
        message_content = json.dumps(message_content)
        body_data = {
            "from_peer": uid,
            "message": message_content,
            "to_peers": group_admin_user,
            "conv_id": LEAN_CLOUD_SYSTEM_CONVERSATION_ID,
            "transient": False,
            "no_sync": True
        }
        body_data = json.dumps(body_data)
        return LeanCloudSystemMessage.send_system_message(body_data)

    @staticmethod
    def send_system_message(request_body=None):
        if request_body is None:
            raise ParamException()
        request_body = json.loads(request_body)
        to_peers_list = request_body['to_peers']
        if to_peers_list is None:
            SendSysMessageFailture()
        list_length = len(to_peers_list)
        if list_length == 0:
            SendSysMessageFailture()
        else:
            split_num = list_length // 20 + 1  # 需要分割的段数
            start_index = 0

            head = [
                "X-LC-Id: " + LEAN_CLOUD_X_LC_Id,
                "X-LC-Key: " + LEAN_CLOUD_X_LC_Key_SYS,
                "Content-Type: application/json"
            ]
            try:
                buffer = BytesIO()
                c = pycurl.Curl()
                c.setopt(c.URL, 'https://leancloud.cn/1.1/rtm/messages')
                c.setopt(pycurl.CUSTOMREQUEST, 'POST')
                c.setopt(c.HTTPHEADER, head)
                # to_peers 太多，分批发送(由于受到lean_cloud的限制)
                while split_num:
                    length = split_num * 20
                    current_to_peers_list = to_peers_list[start_index:length]
                    request_body['to_peers'] = current_to_peers_list
                    request_body = json.dumps(request_body)
                    split_num -= 1
                    start_index += 20
                    c.setopt(c.POSTFIELDS, request_body)
                    c.setopt(c.WRITEDATA, buffer)
                    c.perform()
                code = c.getinfo(c.HTTP_CODE)
                body = buffer.getvalue()
                c.close()
                return code, body.decode()
            except:
                return 500, None
