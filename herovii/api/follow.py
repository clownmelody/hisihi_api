# -*- coding: utf-8 -*-
from flask import json, request
from flask.globals import g

from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import JSONStyleError
from herovii.module.releationship import Relationship
from herovii.libs.bpbase import auth
from herovii.service.forum import add_fans_count_to_recommend_users_info

__author__ = 'shaolei'

api = ApiBlueprint('follow')


@api.route('/recommend_users', methods=['GET'])
@auth.login_required
def get_recommend_users():
    # 返回推荐用户列表
    if not hasattr(g, 'user'):
        rts = Relationship(0)
    elif g.user[1] == 100:
        # 未登陆调用
        rts = Relationship(0)
    else:
        rts = Relationship(g.user[0])
    user_list = rts.merge_recommend_users()
    headers = {'Content-Type': 'application/json'}
    return json.dumps(user_list), 200, headers


@api.route('/2.96/recommend_users', methods=['GET'])
@auth.login_required
def get_recommend_users_v_2_9_6():
    # 返回推荐用户列表
    if not hasattr(g, 'user'):
        rts = Relationship(0)
    elif g.user[1] == 100:
        # 未登陆调用
        rts = Relationship(0)
    else:
        rts = Relationship(g.user[0])
    user_list = rts.merge_recommend_users()
    user_list['users'] = add_fans_count_to_recommend_users_info(user_list['users'])
    headers = {'Content-Type': 'application/json'}
    return json.dumps(user_list), 200, headers


@api.route('/follow_user', methods=['POST'])
@auth.login_required
def follow_user():
    json_data = request.get_json(force=True, silent=True)
    if not json_data:
        try:
            follow_uid = request.values.get('uid')
            recommend_id = request.values.get('recommend_id')
            recommend_type = request.values.get('recommend_type')
        except:
            raise JSONStyleError()
    else:
        follow_uid = json_data['uid']
        recommend_id = json_data['recommend_id']
        recommend_type = json_data['recommend_type']
    rts = Relationship(g.user[0])
    is_follow = rts.follow_user(follow_uid)
    headers = {'Content-Type': 'application/json'}
    if is_follow:
        recommend_id = recommend_id.split(',')
        user = rts.return_another_recommend_user(recommend_type, recommend_id)
        if not user:
            data = {
                'info': '关注成功',
                'user': None
            }
            return json.dumps(data), 201, headers
        data = {
            'info': '关注成功',
            'user': user
        }
        return json.dumps(data), 201, headers
    else:
        data = {
            'info': '您已经关注过了',
            'user': None
        }
        return json.dumps(data), 201, headers

