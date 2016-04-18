# -*- coding: utf-8 -*-
from flask import json
from flask.globals import g

from herovii.libs.bpbase import ApiBlueprint
from herovii.module.releationship import Relationship
from herovii.validator.forms import FollowUserForm
from herovii.libs.bpbase import auth

__author__ = 'shaolei'

api = ApiBlueprint('follow')


@api.route('/recommend_users', methods=['GET'])
def get_recommend_users():
    # 返回推荐用户列表
    if not hasattr(g, 'user'):
        rts = Relationship(0)
    else:
        rts = Relationship(g.user[0])
    user_list = rts.merge_recommend_users()
    headers = {'Content-Type': 'application/json'}
    return json.dumps(user_list), 200, headers


@api.route('/follow_user', methods=['POST'])
@auth.login_required
def follow_user():
    form = FollowUserForm().create_api_form()
    follow_uid = form.uid.data
    recommend_id = form.recommend_id.data
    recommend_type = form.recommend_type.data
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

