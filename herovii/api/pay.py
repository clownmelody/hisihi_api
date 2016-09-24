# -*- coding: utf-8 -*-
from flask import json, request
from flask.globals import g

from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import JSONStyleError
from herovii.libs.bpbase import auth
from herovii.module.order import Order
from herovii.libs.error_code import CreateOrderFailure
from herovii.validator.forms import PagingForm
from herovii.module.wxpay import WeixinPay

__author__ = 'shaolei'

api = ApiBlueprint('pay')
wx_pay = WeixinPay()


@api.route('/create/pay/<int:oid>/<int:type>', methods=['GET'])
@auth.login_required
def create_pay_order(oid, type):
    order = Order(g.user[0])
    # order = Order(72)
    data = order.get_order_detail(oid)
    body = 'hisihi-rebate'
    # total_fee = int(data['price']) * 100
    total_fee = 1
    obj = wx_pay.unified_order(out_trade_no=data['order_sn'], body=body, total_fee=total_fee,
                               trade_type='APP')
    headers = {'Content-Type': 'application/json'}
    if obj:
        app_data = wx_pay.second_sign(prepayid=obj['prepay_id'])
        return json.dumps(app_data), 200, headers
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


@api.route("/wxpay/notify")
def wxpay_notify():
    """
    微信异步通知
    """
    data = wx_pay.to_dict(request.data)
    if not wx_pay.check(data):
        return wx_pay.reply("签名验证失败", False)
    # 处理业务逻辑
    order = Order()
    order.update_order_status(5, 1)
    return wx_pay.reply("OK", True)

