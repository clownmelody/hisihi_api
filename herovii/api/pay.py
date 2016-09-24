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


@api.route('/create/pay/<int:type>', methods=['POST'])
# @auth.login_required
def create_pay_order(type):
    data = request.get_json(force=True, silent=True)
    wx_pay = WeixinPay(None)
    obj = wx_pay.unified_order(out_trade_no=data['out_trade_no'], body=data['body'], total_fee=data['total_fee'],
                               trade_type=data['trade_type'])
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


@api.route("/wxpay/notify")
def wxpay_notify():
    """
    微信异步通知
    """
    wx_pay = WeixinPay()
    data = wx_pay.to_dict(request.data)
    if not wx_pay.check(data):
        return wx_pay.reply("签名验证失败", False)
    # 处理业务逻辑
    return wx_pay.reply("OK", True)

