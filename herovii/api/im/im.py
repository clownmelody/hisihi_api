# -*- coding: utf-8 -*-
import json
from flask import current_app
from herovii.libs.bpbase import ApiBlueprint
from herovii.service.im import sign, get_timestamp, get_nonce

__author__ = 'yangchujie'

api = ApiBlueprint('im')


@api.route('/signature/login/<string:app_id>/<string:client_id>', methods=['GET'])
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
