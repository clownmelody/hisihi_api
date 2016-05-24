# -*- coding: utf-8 -*-
import json
from herovii.models.user.user_csu import UserCSU
from herovii.models.user.user_csu_secure import UserCSUSecure
from herovii.service.org import get_coupon_list_by_uid
from herovii.service.user_csu import db_change_indentity
from flask import jsonify, request
from herovii.validator.forms import PhoneNumberForm, \
    UserCSUChangeIdentityForm, PagingForm
from herovii.service import user_org
from herovii.validator import user_verify
from herovii.libs.error_code import NotFound
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.bpbase import auth

__author__ = 'bliss'

api = ApiBlueprint('user')


@api.route('/csu', methods=['POST'])
def create_csu_user():
    pass


@api.route('/csu/identity', methods=["PUT"])
@auth.login_required
def change_identity():
    """改变CSU用户操作组"""
    form = UserCSUChangeIdentityForm.create_api_form()
    id_realation = db_change_indentity(form.uid.data, form.group_id.data)
    return jsonify(id_realation), 202


@api.route('/csu', methods=['GET'])
# @auth.login_required
def get_csu():
    s = request.args
    form = PhoneNumberForm.create_api_form(**request.args.to_dict())
    mobile = form.mobile.data
    if mobile:
        user = UserCSU.query.filter_by(mobile=mobile).first_or_404()
        return jsonify(user), 200
    else:
        raise NotFound(error_code=2000, error='user not found')


@api.route('/csu', methods=['PUT'])
def update_csu():
    pass


@api.route('/csu/<int:uid>', methods=['GET'])
# @auth.login_required
def get_user_uid(uid):
    uid = user_verify.verify_uid(uid)
    user = user_org.get_user_by_uid(uid)
    if user:
        return jsonify(user), 200
    else:
        raise NotFound('user not found', 2000)


@api.route('/<int:uid>/coupons')
@auth.login_required
def get_user_coupon_list(uid):
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    total_count, coupon_list = get_coupon_list_by_uid(uid, form.page.data, form.per_page.data)
    result = {
        "total_count": total_count,
        "data": coupon_list
    }
    json_data = json.dumps(result)
    headers = {'Content-Type': 'application/json'}
    return json_data, 200, headers

