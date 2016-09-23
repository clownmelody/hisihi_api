# -*- coding: utf-8 -*-
from flask import json, request
from flask.globals import g

from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import JSONStyleError
from herovii.libs.bpbase import auth
from herovii.module.order import Order
from herovii.libs.error_code import CreateOrderFailure
from herovii.validator.forms import PagingForm

__author__ = 'shaolei'

api = ApiBlueprint('order')


@api.route('/list', methods=['GET'])
@auth.login_required
def get_user_order_list():
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    order = Order(g.user[0])
    # order = Order(71)
    count, order_list = order.get_user_order_list(page, per_page)
    headers = {'Content-Type': 'application/json'}
    data = {
        'count': count,
        'data': order_list
    }
    return json.dumps(data), 200, headers


@api.route('/create', methods=['POST'])
@auth.login_required
def create_order():
    json_data = request.get_json(force=True, silent=True)
    if not json_data:
        try:
            mobile = request.values.get('mobile')
            courses_id = request.values.get('courses_id')
            rebate_id = request.values.get('rebate_id')
            num = request.values.get('num')
        except:
            raise JSONStyleError()
    else:
        mobile = json_data['mobile']
        courses_id = json_data['courses_id']
        rebate_id = json_data['rebate_id']
        num = json_data['num']
    order = Order(g.user[0])
    # order = Order(72)
    obj = order.create_order(mobile, courses_id, rebate_id, num)
    headers = {'Content-Type': 'application/json'}
    if obj:
        return json.dumps(obj), 201, headers
    else:
        raise CreateOrderFailure()


@api.route('/detail/<int:oid>', methods=['GET'])
@auth.login_required
def get_order_detail(oid):
    order = Order(g.user[0])
    # order = Order(72)
    obj = order.get_order_detail(oid)
    headers = {'Content-Type': 'application/json'}
    return json.dumps(obj), 200, headers


