# -*- coding: utf-8 -*-
from flask import json, request
from flask.globals import g
import urllib
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import RebateExpiredFailure, \
    RebateIsDisabledFailure
from herovii.libs.bpbase import auth
from herovii.module.alipay import AliPay
from herovii.module.order import Order
from herovii.libs.error_code import CreateOrderFailure
from herovii.module.wxpay import WeixinPay
from flask import current_app

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
        payment_info = ali_pay.make_payment_info2(out_trade_no=data['order_sn'], subject='heishehui.cn',
                                                  total_fee=total_fee, body=body)
        res = ali_pay.make_payment_request2(payment_info)
        data = {
            'data': res
        }
        order.update_order_pay_type(oid, type)
        return json.dumps(data), 200, headers
    else:
        #微信支付
        body = 'heishehui.cn'
        # total_fee = int(data['price']) * 100
        total_fee = 1
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
        pay_type = order.get_order_pay_type(oid)
        if not pay_type:
            app_data = {
                    'pay_status': 0
                }
            return json.dumps(app_data), 200, headers
        if pay_type == 1:
            params = ali_pay.make_trade_query_info(out_trade_no=data['order_sn'])
            obj = ali_pay.query_trade_status(params)
            if obj:
                pay_status = 1
                user_rebate_id = order.get_user_rebate_id(oid)
                app_data = {
                    'pay_status': pay_status,
                    'user_rebate_id': user_rebate_id
                }
            else:
                app_data = {
                    'pay_status': 0
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
    params_str = urllib.parse.urlencode(request.values)
    current_app.logger.warn(params_str)
    params = request.values
    sign = params['sign']
    params = ali_pay.params_filter(params)
    for key in sorted(params.keys(), reverse=False):
        value = params[key]
        params[key] = urllib.parse.unquote_plus(value)
    message = ali_pay.params_to_query(params, quotes=False, reverse=False)
    current_app.logger.warn('message====>' + message)
    check_res = ali_pay.check_ali_sign(message, sign)
    if not check_res:
        return 'false'
    # 处理业务逻辑
    order = Order()
    res = order.check_order_status(params['out_trade_no'])
    if res:
        return 'success'
    else:
        if params['trade_status'] == 'TRADE_SUCCESS' or params['trade_status'] == 'TRADE_FINISHED':
            cur_order = order.get_order_by_ordersn(params['out_trade_no'])
            if params['total_amount'] == '0.01'\
                    and params['seller_id'] == current_app.config['ALI_PARTNER_ID']\
                    and params['app_id'] == current_app.config['ALI_APP_ID']:
                order.create_user_rebate(params['out_trade_no'])
                order.update_order_status(params['out_trade_no'], 1)
                order.update_order_pay_time(params['out_trade_no'])
                return 'success'

