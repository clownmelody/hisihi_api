# -*- coding: utf-8 -*-
from flask import json, request
from flask.globals import g

from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import JSONStyleError, OrderAlreadyPayFailure
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
    headers = {'Content-Type': 'application/json'}
    order = Order(g.user[0])
    # order = Order(72)
    data = order.get_order_detail(oid)
    if data['order_status'] > 0:
        pay_status = 1
        user_rebate_id = order.get_user_rebate_id(oid)
        app_data = {
            'pay_status': pay_status,
            'user_rebate_id': user_rebate_id
        }
        return json.dumps(app_data), 200, headers
    body = 'hisihi-rebate'
    # total_fee = int(data['price']) * 100
    total_fee = 1
    obj = wx_pay.unified_order(out_trade_no=data['order_sn'], body=body, total_fee=total_fee,
                               trade_type='APP')
    if obj:
        app_data = wx_pay.second_sign(prepayid=obj['prepay_id'])
        app_data.setdefault('pay_status', 0)
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


@api.route("/wxpay/notify", methods=['POST'])
def wxpay_notify():
    """
    微信异步通知
    """
    req = request.stream.read()
    data = wx_pay.to_dict(req)
    if not wx_pay.check(data):
        return wx_pay.reply("签名验证失败", False)
    # 处理业务逻辑
    order = Order()
    res = order.check_order_status(data['out_trade_no'])
    if res:
        return wx_pay.reply("OK", True)
    else:
        order.create_user_rebate(data['out_trade_no'])
        order.update_order_status(data['out_trade_no'], 1)
        return wx_pay.reply("OK", True)


