# -*- coding: utf-8 -*-
from flask import json, request
from flask.globals import g

from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import RebateExpiredFailure, \
    RebateIsDisabledFailure
from herovii.libs.bpbase import auth
from herovii.module.alipay import AliPay
from herovii.module.order import Order
from herovii.libs.error_code import CreateOrderFailure
from herovii.module.wxpay import WeixinPay

__author__ = 'shaolei'

api = ApiBlueprint('pay')
wx_pay = WeixinPay()
ali_pay = AliPay()


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
    if data['rebate']['is_disabled']:
        raise RebateIsDisabledFailure()
    rebate = order.get_rebate_info(data['rebate']['id'])
    is_out_of_date = order.is_out_of_date(rebate)
    if is_out_of_date:
        raise RebateExpiredFailure()
    if type > 0:
        #支付宝支付
        #构造订单信息
        # total_fee = int(data['price'])
        total_fee = 0.01  #这里讲金额设为1分钱，方便测试
        body = "heishehui.cn"
        payment_info = ali_pay.make_payment_info(out_trade_no=data['order_sn'], subject='heishehui.cn', total_fee=total_fee,
                                                 body=body)
        res = ali_pay.make_payment_request(payment_info)
        data = {
            'data': res
        }
        return json.dumps(data), 200, headers
    else:
        #微信支付
        body = 'heishehui.cn'
        total_fee = int(data['price']) * 100
        # total_fee = 1
        obj = wx_pay.unified_order(out_trade_no=data['order_sn'], body=body, total_fee=total_fee,
                                   trade_type='APP')
        if obj:
            app_data = wx_pay.second_sign(prepayid=obj['prepay_id'])
            app_data.setdefault('pay_status', 0)
            order.update_order_pay_type(oid, type)
            return json.dumps(app_data), 200, headers
        else:
            raise CreateOrderFailure()


@api.route('/order/query/<int:oid>', methods=['GET'])
@auth.login_required
def get_order_detail(oid):
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
    else:
        obj = wx_pay.order_query(out_trade_no=data['order_sn'])
        if obj['trade_state'] == 'SUCCESS':
            pay_status = 1
            user_rebate_id = order.get_user_rebate_id(oid)
            app_data = {
                'pay_status': pay_status,
                'user_rebate_id': user_rebate_id
            }
        elif obj['trade_state'] == 'USERPAYING':
            app_data = {
                'pay_status': 2
            }
        else:
            app_data = {
                'pay_status': 0
            }
        return json.dumps(app_data), 200, headers


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
        order.update_order_pay_time(data['out_trade_no'])
        return wx_pay.reply("OK", True)


@api.route("/alipay/notify", methods=['POST'])
def alipay_notify():
    """
    支付宝异步通知
    """
    req = request.stream.read()
    params = ali_pay.query_to_dict(req.decode('utf-8'))
    sign = params['sign']
    #sign = sign.decode('utf-8')
    params = ali_pay.params_filter(params)
    message = ali_pay.params_to_query(params, quotes=False, reverse=False)
    check_res = ali_pay.check_ali_sign(message, sign)
    assert check_res == True
    res = ali_pay.verify_from_gateway({"partner": ali_pay.app.config['ALI_PARTNER_ID'], "notify_id": params["notify_id"]})
    assert res == False
    # 处理业务逻辑
    order = Order()
    res = order.check_order_status(params['out_trade_no'])
    if res:
        return wx_pay.reply("OK", True)
    else:
        order.create_user_rebate(params['out_trade_no'])
        order.update_order_status(params['out_trade_no'], 1)
        order.update_order_pay_time(params['out_trade_no'])
        return wx_pay.reply("OK", True)

