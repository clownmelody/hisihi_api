# -*- coding: utf-8 -*-
import json

from flask.globals import g

from herovii import db
from herovii.models.user.user_coupon import UserCoupon
from herovii.models.user.user_csu import UserCSU
from herovii.service.org import get_coupon_detail_by_uid, get_coupon_detail_by_uid_v2_9_2
from herovii.models.user.user_gift_package import UserGiftPackage
from herovii.service.org import get_coupon_list_by_uid, is_coupon_out_of_date, get_teaching_course_coupon_code_service
from herovii.service.user_csu import db_change_indentity
from flask import jsonify, request
from herovii.validator.forms import PhoneNumberForm, \
    UserCSUChangeIdentityForm, PagingForm, ObtainCouponForm, ObtainGiftPackageForm
from herovii.service import user_org
from herovii.validator import user_verify
from herovii.libs.error_code import NotFound, CouponOutOfDateFailture, CouponHasObtainedFailture, \
    GiftHasObtainedFailture
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.bpbase import auth
from herovii.service.rebate import get_rebate_list_by_uid

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


@api.route('/coupons', methods=['POST'])
@auth.login_required
def add_coupon_to_user():
    if not hasattr(g, 'user'):
        uid = 0
    elif g.user[1] == 100:
        uid = 0
    else:
        uid = g.user[0]
    form = ObtainCouponForm.create_api_form()
    user_coupon = UserCoupon()
    for key, value in form.body_data.items():
        setattr(user_coupon, key, value)
    user_coupon.uid = uid
    is_obtain = db.session.query(UserCoupon).filter(UserCoupon.uid == user_coupon.uid,
                                                    UserCoupon.coupon_id == user_coupon.coupon_id,
                                                    UserCoupon.teaching_course_id == form.teaching_course_id.data,
                                                    UserCoupon.status != -1) \
        .first()
    if is_obtain:
        data = {
            'obtain_id': is_obtain.id,
            'has_obtained': True
        }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        return json_data, 201, headers
    else:
        promo_code, promo_code_url = get_teaching_course_coupon_code_service(uid)
        user_coupon.promo_code = promo_code
        user_coupon.promo_code_url = promo_code_url
        if is_coupon_out_of_date(user_coupon.coupon_id):
            raise CouponOutOfDateFailture()
        with db.auto_commit():
            db.session.add(user_coupon)
        data = {
                'obtain_id': user_coupon.id,
                'has_obtained': False
            }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        return json_data, 201, headers


@api.route('/coupon/<int:id>/detail', methods=['GET'])
@auth.login_required
def get_user_coupon_detail(id):
    coupon = get_coupon_detail_by_uid(id)
    return jsonify(coupon), 200


@api.route('/2.92/coupon/<int:id>/detail', methods=['GET'])
@auth.login_required
def get_user_coupon_detail_v2_9_2(id):
    coupon = get_coupon_detail_by_uid_v2_9_2(id)
    return jsonify(coupon), 200


@api.route('/gift_package', methods=['POST'])
@auth.login_required
def user_get_gift_package():
    form = ObtainGiftPackageForm.create_api_form()
    user_gift_package = UserGiftPackage()
    for key, value in form.body_data.items():
        setattr(user_gift_package, key, value)
    is_obtain = db.session.query(UserGiftPackage).filter(UserGiftPackage.uid == user_gift_package.uid,
                                                         UserGiftPackage.obtain_coupon_record_id == user_gift_package.obtain_coupon_record_id,
                                                         UserGiftPackage.status != -1) \
        .count()
    if is_obtain:
        raise GiftHasObtainedFailture()
    with db.auto_commit():
        db.session.add(user_gift_package)
    return jsonify(user_gift_package), 201


@api.route('/2.92/gift_package', methods=['POST'])
@auth.login_required
def user_get_gift_package_v2_9_2():
    form = ObtainGiftPackageForm.create_api_form()
    user_gift_package = UserGiftPackage()
    for key, value in form.body_data.items():
        setattr(user_gift_package, key, value)
    is_obtain = db.session.query(UserGiftPackage)\
        .filter(UserGiftPackage.uid == user_gift_package.uid,
                UserGiftPackage.obtain_coupon_record_id == user_gift_package.obtain_coupon_record_id,
                UserGiftPackage.status != -1) \
        .count()
    if is_obtain:
        raise GiftHasObtainedFailture()
    with db.auto_commit():
        db.session.add(user_gift_package)
    return jsonify(user_gift_package), 201


@api.route('/<int:uid>/rebate/<int:type>')
@auth.login_required
def get_user_rebate_list(uid, type):
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    total_count, rebate_list = get_rebate_list_by_uid(uid, type, form.page.data, form.per_page.data)
    result = {
        "count": total_count,
        "data": rebate_list
    }
    json_data = json.dumps(result)
    headers = {'Content-Type': 'application/json'}
    return json_data, 200, headers
