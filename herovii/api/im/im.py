# -*- coding: utf-8 -*-
import json
from flask import current_app, request, g
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import CreateImGroupFailture, UpdateImGroupFailture, ParamException, DeleteImGroupFailture, \
    DeleteImGroupMemberFailture, AddGroupMemberFailture
from herovii.libs.util import parse_page_args
from herovii.service.im import sign, get_timestamp, get_nonce, create_im_group_service, update_im_group_service, \
    delete_im_group_service, add_im_group_members_service, delete_im_group_members_service, \
    get_organization_im_groups_service, get_organization_im_contacts_service, push_message_to_all_classmates_service, \
    dismiss_im_group_service, get_im_user_groups_service, get_im_group_detail_service, is_client_id_in_group_member, \
    get_all_im_groups_service
from herovii.validator.forms import PagingForm

__author__ = 'yangchujie'

api = ApiBlueprint('im')


@api.route('/signature/login/<string:app_id>/<string:client_id>', methods=['GET'])
# @auth.login_required
# 登陆签名
def get_im_login_signature(app_id, client_id):
    master_key = current_app.config['LEAN_CLOUD_MASTER_KEY']
    timestamp = get_timestamp()
    nonce = get_nonce()
    var_list = [app_id, client_id]
    split_symbol = ':'
    msg = split_symbol.join(var_list) + '::' + str(timestamp) + ':' + nonce
    signature = sign(msg, master_key)
    result = {
        'app_id': app_id,
        'client_id': client_id,
        'timestamp': timestamp,
        'nonce': nonce,
        'signature': signature
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/signature/conversation/<string:app_id>/<string:client_id>/<string:sorted_member_ids>', methods=['GET'])
# @auth.login_required
# 开启会话签名
def get_im_start_conversation_signature(app_id, client_id, sorted_member_ids):
    master_key = current_app.config['LEAN_CLOUD_MASTER_KEY']
    timestamp = get_timestamp()
    nonce = get_nonce()
    var_list = [app_id, client_id, sorted_member_ids, str(timestamp), nonce]
    split_symbol = ':'
    msg = split_symbol.join(var_list)
    signature = sign(msg, master_key)
    result = {
        'app_id': app_id,
        'client_id': client_id,
        'sorted_member_ids': sorted_member_ids,
        'timestamp': timestamp,
        'nonce': nonce,
        'signature': signature
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/signature/invite/<string:app_id>/<string:client_id>/<string:conversation_id>/<string:sorted_member_ids>',
           methods=['GET'])
# @auth.login_required
# 群组加人操作签名
def get_im_invite_signature(app_id, client_id, conversation_id, sorted_member_ids):
    master_key = current_app.config['LEAN_CLOUD_MASTER_KEY']
    timestamp = get_timestamp()
    nonce = get_nonce()
    var_list = [app_id, client_id, conversation_id, sorted_member_ids, str(timestamp), nonce, 'invite']
    split_symbol = ':'
    msg = split_symbol.join(var_list)
    signature = sign(msg, master_key)
    result = {
        'app_id': app_id,
        'client_id': client_id,
        'conversation_id': conversation_id,
        'sorted_member_ids': sorted_member_ids,
        'timestamp': timestamp,
        'nonce': nonce,
        'signature': signature,
        'action': 'invite'
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/signature/kick/<string:app_id>/<string:client_id>/<string:conversation_id>/<string:sorted_member_ids>',
           methods=['GET'])
# @auth.login_required
# 群组删人签名
def get_im_kick_signature(app_id, client_id, conversation_id, sorted_member_ids):
    master_key = current_app.config['LEAN_CLOUD_MASTER_KEY']
    timestamp = get_timestamp()
    nonce = get_nonce()
    var_list = [app_id, client_id, conversation_id, sorted_member_ids, str(timestamp), nonce, 'kick']
    split_symbol = ':'
    msg = split_symbol.join(var_list)
    signature = sign(msg, master_key)
    result = {
        'app_id': app_id,
        'client_id': client_id,
        'conversation_id': conversation_id,
        'sorted_member_ids': sorted_member_ids,
        'timestamp': timestamp,
        'nonce': nonce,
        'signature': signature,
        'action': 'kick'
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


# @api.route('/signature/join/<string:app_id>/<string:client_id>/<string:conversation_id>/<string:sorted_member_ids>',
#            methods=['GET'])
# # 加入群操作签名
# def get_im_join_signature(app_id, client_id, conversation_id, sorted_member_ids):
#     master_key = current_app.config['LEANCLOUD_SECRET_KEY']
#     timestamp = get_timestamp()
#     nonce = get_nonce()
#     var_list = [app_id, client_id, conversation_id, sorted_member_ids, timestamp, nonce, 'join']
#     split_symbol = ':'
#     msg = split_symbol.join(var_list)
#     print(msg)
#     signature = sign(msg, master_key)
#     result = {
#         'app_id': app_id,
#         'client_id': client_id,
#         'conversation_id': conversation_id,
#         'sorted_member_ids': sorted_member_ids,
#         'timestamp': timestamp,
#         'nonce': nonce,
#         'signature': signature,
#         'action': 'join'
#     }
#     headers = {'Content-Type': 'application/json'}
#     return json.dumps(result), 200, headers


@api.route('/group', methods=['POST'])
# @auth.login_required
# 创建群组
def create_im_group():
    request_json = request.get_json(force=True, silent=True)
    group_name = request_json['group_name']
    member_client_ids = request_json['member_client_ids']
    organization_id = request_json['organization_id']
    conversation_id = request_json['conversation_id']
    group_avatar = request_json['group_avatar']
    description = request_json['description']
    admin_uid = request_json['admin_uid']
    if organization_id == 0 or group_avatar is None or admin_uid is None or group_name is None \
            or description is None:
        raise ParamException()
    group_id, conversation_id, result = create_im_group_service(group_name, member_client_ids, organization_id,
                                                                conversation_id, group_avatar, admin_uid, description)
    if result:
        result = {
            'group_id': group_id,
            'group_name': group_name,
            'member_client_ids': member_client_ids,
            'organization_id': organization_id,
            'conversation_id': conversation_id,
            'group_avatar': group_avatar,
            'admin_uid': admin_uid,
            'description': description
        }
    else:
        raise CreateImGroupFailture()
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 201, headers


@api.route('/group/<int:group_id>', methods=['PUT'])
# @auth.login_required
# 修改群组信息
def update_im_group(group_id=0):
    if group_id == 0:
        raise ParamException()
    request_json = request.get_json(force=True, silent=True)
    group_name = request_json['group_name']
    if group_name is None:
        group_name = "群聊"
    result = update_im_group_service(group_id, group_name)
    if result:
        result = {
            'group_name': group_name,
        }
    else:
        raise UpdateImGroupFailture()
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/group/<int:group_id>', methods=['DELETE'])
# @auth.login_required
# 删除群组
def delete_im_group(group_id=0):
    if group_id == 0:
        raise ParamException()
    result = delete_im_group_service(group_id)
    if not result:
        raise DeleteImGroupFailture()
    return '', 204


@api.route('/user/<int:uid>/group/<int:group_id>', methods=['DELETE'])
# @auth.login_required
# 管理员解散群组
def dismiss_im_group(uid=0, group_id=0):
    if uid == 0 or group_id == 0:
        raise ParamException()
    result = dismiss_im_group_service(uid, group_id)
    if not result:
        raise DeleteImGroupFailture()
    return '', 204


@api.route('/group/<int:group_id>/member', methods=['POST'])
# @auth.login_required
# 添加群成员
def add_im_group_members(group_id=0):
    if group_id == 0:
        raise ParamException()
    request_json = request.get_json(force=True, silent=True)
    member_client_ids = request_json['member_client_ids']
    if member_client_ids is None:
        raise ParamException()
    result = add_im_group_members_service(group_id, member_client_ids)
    if result:
        result = {
            'group_id': group_id,
            'member_client_ids': member_client_ids
        }
    else:
        raise AddGroupMemberFailture()
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 201, headers


@api.route('/group/<int:group_id>/member/<string:client_id>', methods=['DELETE'])
@auth.login_required
# 删除群成员
def delete_im_group_members(group_id=0, client_id=None):
    if group_id == 0 or client_id is None:
        raise ParamException()
    user_info = g.user
    uid = user_info[0]
    token_client_id = 'c' + str(uid)
    if token_client_id == client_id:  # 用户主动退群
        result = delete_im_group_members_service(group_id, client_id, True)
    else:  # 群主移除用户
        result = delete_im_group_members_service(group_id, client_id, False)
    if not result:
        raise DeleteImGroupMemberFailture()
    return '', 204


@api.route('/org/<int:organization_id>/groups', methods=['GET'])
# @auth.login_required
# 获取机构下所有群组
def get_organization_im_groups(organization_id=0):
    if organization_id == 0:
        raise ParamException()
    request_json = request.get_json(force=True, silent=True)
    page, per_page = parse_page_args(request_json)
    total_count, data = get_organization_im_groups_service(organization_id, page, per_page)
    result = {
        "total_count": total_count,
        "data": data
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/groups', methods=['GET'])
# @auth.login_required
# 获取所有机构所有群组列表
def get_all_im_groups():
    request_json = request.get_json(force=True, silent=True)
    page, per_page = parse_page_args(request_json)
    total_count, data = get_all_im_groups_service(page, per_page)
    result = {
        "total_count": total_count,
        "data": data
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/org/<int:organization_id>/contacts', methods=['GET'])
@auth.login_required
# 获取机构下所有联系人
def get_organization_im_contacts(organization_id=0):
    if organization_id == 0:
        raise ParamException()
    data = get_organization_im_contacts_service(organization_id)
    result = {
        "data": data
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/org/<int:class_id>/message', methods=['POST'])
# @auth.login_required
# 向班级学生群发通知
def push_message_to_all_classmates(class_id=0):
    # message = request.form.get('message', None)
    # if class_id == 0 or message is None:
    #     raise ParamException()
    if class_id == 0:
        raise ParamException()
    history_id = push_message_to_all_classmates_service(class_id)
    result = {
        "class_id": class_id,
        "push_history_record_id": history_id
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 201, headers


@api.route('/user/<string:client_id>/groups', methods=['GET'])
# 获取用户的所有群组
def get_im_user_groups(client_id=0):
    if client_id == 0:
        raise ParamException()
    data = get_im_user_groups_service(client_id)
    result = {
        "data": data
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/group/<int:group_id>', methods=['GET'])
# 获取群组详情
def get_im_group_detail(group_id=0):
    if group_id == 0:
        raise ParamException()
    data = get_im_group_detail_service(group_id)
    result = {
        "data": data
    }
    client_id = request.args.get("client_id")
    if client_id is not None:
        is_exist_in_group = is_client_id_in_group_member(group_id, client_id)
        result['is_exist_in_group'] = is_exist_in_group
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/user/<string:client_id>/group/<int:group_id>/join_group_notification', methods=['POST'])
# @auth.login_required
# 用户加群通知
def user_join_group_notification(client_id=None, group_id=0):
    if client_id is None or group_id == 0:
        raise ParamException()
    from herovii.libs.lean_cloud_system_message import LeanCloudSystemMessage
    is_exist_in_group = is_client_id_in_group_member(group_id, client_id)
    if is_exist_in_group:  # 用户已在该群中
        result = {
            "code": 7009,
            "message": "用户已在该群组中"
        }
        headers = {'Content-Type': 'application/json'}
        return json.dumps(result), 400, headers
    code, resp = LeanCloudSystemMessage.push_user_join_in_group_apply_message(client_id, group_id)
    if code // 100 == 2:
        result = {
            "message": "已为您提交加群申请"
        }
    else:
        result = {
            "message": resp
        }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 201, headers
