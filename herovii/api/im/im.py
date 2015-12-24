# -*- coding: utf-8 -*-
import json
from flask import current_app, request
from werkzeug.exceptions import RequestEntityTooLarge
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import CreateImGroupFailture, UpdateImGroupFailture, ParamException, DeleteImGroupFailture, \
    DeleteImGroupMemberFailture
from herovii.service.file import FilePiper
from herovii.service.im import sign, get_timestamp, get_nonce, create_im_group_service, update_im_group_service, \
    delete_im_group_service, add_im_group_members_service, delete_im_group_members_service, \
    get_organization_im_groups_service, get_organization_im_contacts_service
from herovii.validator.forms import PagingForm

__author__ = 'yangchujie'

api = ApiBlueprint('im')


@api.route('/signature/login/<string:app_id>/<string:client_id>', methods=['GET'])
@auth.login_required
# 登陆签名
def get_im_login_signature(app_id, client_id):
    master_key = current_app.config['LEANCLOUD_SECRET_KEY']
    timestamp = get_timestamp()
    nonce = get_nonce()
    var_list = [app_id, client_id]
    split_symbol = ':'
    msg = split_symbol.join(var_list) + '::' + timestamp + ':' + nonce
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


@api.route('/signature/conversion/<string:app_id>/<string:client_id>/<string:sorted_member_ids>', methods=['GET'])
@auth.login_required
# 开启会话签名
def get_im_start_conversion_signature(app_id, client_id, sorted_member_ids):
    master_key = current_app.config['LEANCLOUD_SECRET_KEY']
    timestamp = get_timestamp()
    nonce = get_nonce()
    var_list = [app_id, client_id, sorted_member_ids, timestamp, nonce]
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


@api.route('/signature/invite/<string:app_id>/<string:client_id>/<string:conversion_id>/<string:sorted_member_ids>',
           methods=['GET'])
@auth.login_required
# 群组加人操作签名
def get_im_invite_signature(app_id, client_id, conversion_id, sorted_member_ids):
    master_key = current_app.config['LEANCLOUD_SECRET_KEY']
    timestamp = get_timestamp()
    nonce = get_nonce()
    var_list = [app_id, client_id, conversion_id, sorted_member_ids, timestamp, nonce, 'invite']
    split_symbol = ':'
    msg = split_symbol.join(var_list)
    signature = sign(msg, master_key)
    result = {
        'app_id': app_id,
        'client_id': client_id,
        'conversion_id': conversion_id,
        'sorted_member_ids': sorted_member_ids,
        'timestamp': timestamp,
        'nonce': nonce,
        'signature': signature,
        'action': 'invite'
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/signature/kick/<string:app_id>/<string:client_id>/<string:conversion_id>/<string:sorted_member_ids>',
           methods=['GET'])
@auth.login_required
# 群组删人签名
def get_im_kick_signature(app_id, client_id, conversion_id, sorted_member_ids):
    master_key = current_app.config['LEANCLOUD_SECRET_KEY']
    timestamp = get_timestamp()
    nonce = get_nonce()
    var_list = [app_id, client_id, conversion_id, sorted_member_ids, timestamp, nonce, 'kick']
    split_symbol = ':'
    msg = split_symbol.join(var_list)
    signature = sign(msg, master_key)
    result = {
        'app_id': app_id,
        'client_id': client_id,
        'conversion_id': conversion_id,
        'sorted_member_ids': sorted_member_ids,
        'timestamp': timestamp,
        'nonce': nonce,
        'signature': signature,
        'action': 'kick'
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


# @api.route('/signature/join/<string:app_id>/<string:client_id>/<string:conversion_id>/<string:sorted_member_ids>',
#            methods=['GET'])
# # 加入群操作签名
# def get_im_join_signature(app_id, client_id, conversion_id, sorted_member_ids):
#     master_key = current_app.config['LEANCLOUD_SECRET_KEY']
#     timestamp = get_timestamp()
#     nonce = get_nonce()
#     var_list = [app_id, client_id, conversion_id, sorted_member_ids, timestamp, nonce, 'join']
#     split_symbol = ':'
#     msg = split_symbol.join(var_list)
#     print(msg)
#     signature = sign(msg, master_key)
#     result = {
#         'app_id': app_id,
#         'client_id': client_id,
#         'conversion_id': conversion_id,
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
    group_name = request.form.get('group_name', '群聊')
    member_client_ids = request.form.get('member_client_ids', None)
    organization_id = request.form.get('organization_id', 0)
    conversion_id = request.form.get('conversion_id', 0)
    group_avatar = request.form.get('group_avatar', '')
    group_id, result = create_im_group_service(group_name, member_client_ids, organization_id, conversion_id, group_avatar)
    if result:
        result = {
            'group_id': group_id,
            'group_name': group_name,
            'member_client_ids': member_client_ids,
            'organization_id': organization_id,
            'conversion_id': conversion_id,
            'group_avatar': group_avatar
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
    group_name = request.form.get('group_name', '群聊')
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


@api.route('/group/<int:group_id>/member', methods=['POST'])
# @auth.login_required
# 添加群成员
def add_im_group_members(group_id=0):
    if group_id == 0:
        raise ParamException()
    member_client_ids = request.form.get('member_client_ids', None)
    result = add_im_group_members_service(group_id, member_client_ids)
    if result:
        result = {
            'group_id': group_id,
            'member_client_ids': member_client_ids
        }
    else:
        raise CreateImGroupFailture()
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 201, headers


@api.route('/group/<int:group_id>/member', methods=['DELETE'])
# @auth.login_required
# 删除群成员
def delete_im_group_members(group_id=0):
    if group_id == 0:
        raise ParamException()
    member_client_ids = request.form.get('member_client_ids', None)
    result = delete_im_group_members_service(group_id, member_client_ids)
    if not result:
        raise DeleteImGroupMemberFailture()
    return '', 204


@api.route('/org/<int:organization_id>/groups', methods=['GET'])
# @auth.login_required
# 获取机构下所有群组
def get_organization_im_groups(organization_id=0):
    if organization_id == 0:
        raise ParamException()
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    total_count, data = get_organization_im_groups_service(organization_id, page, per_page)
    result = {
        "total_count": total_count,
        "data": data
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/org/<int:organization_id>/contacts', methods=['GET'])
# @auth.login_required
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
