#coding:utf-8
import rsa
import base64
import urllib
import requests
import hashlib
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
import json
import datetime
from flask import current_app

SIGN_TYPE = "SHA-1"
__author__ = 'shaolei'


class AliPayError(Exception):

    def __init__(self, msg):
        super(AliPayError, self).__init__(msg)


class AliPay(object):
    def __init__(self):
        self.app = current_app

    def params_filter(self, params):
        """
        去掉不需要验证前面的参数
        :param params:
        :return:
        """
        ret = {}
        for key, value in params.items():
            if key == "sign" or key == "sign_type" or value == "":
                continue
            ret[key] = value
        return ret

    def query_to_dict(self, query):
        """
        将query string转换成字典
        :param query:
        :return:
        """
        res = {}
        k_v_pairs = query.split("&")
        for item in k_v_pairs:
            sp_item = item.split("=", 1)  #注意这里，因为sign秘钥里面肯那个包含'='符号，所以splint一次就可以了
            key = sp_item[0]
            value = sp_item[1]
            res[key] = value

        return res

    def params_to_query(self, params, quotes=False, reverse=False):
        """
            生成需要签名的字符串
        :param params:
        :return:
        """
        query = ""
        for key in sorted(params.keys(), reverse=reverse):
            value = params[key]
            if quotes == True:
                query += str(key) + "=\"" + str(value) + "\"&"
            else:
                query += str(key) + "=" + str(value) + "&"
        query = query[0:-1]
        return query

    def make_sign(self, message):
        """
        签名
        :param message:
        :return:
        """
        # cur_path = os.path.abspath('.')
        # current_app.logger.warn(cur_path)
        # current_app.logger.error(cur_path)
        with open(self.app.config['RSA_PRIVATE_PATH']) as privatefile:
            keydata = privatefile.read()
        key = RSA.importKey(keydata)
        h = SHA.new()
        m_str = message.encode('utf-8')
        h.update(m_str)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(h)
        s = b64encode(signature)
        return s

    def make_sign2(self, message):
        """
        签名
        :param message:
        :return:
        """
        with open(self.app.config['RSA_PRIVATE_PATH'], 'rb') as privatefile:
            keydata = privatefile.read()
        private_key = rsa.PrivateKey._load_pkcs1_pem(current_app.config['RSA_PRIVATE'])
        sign = rsa.sign(message, private_key, SIGN_TYPE)
        b64sing = base64.b64encode(sign)
        return b64sing

    def make_sign3(self, message):
        """
        签名
        :param message:
        :return:
        """
        with open(self.app.config['RSA_PRIVATE_PATH']) as privatefile:
            keydata = privatefile.read()
        key = RSA.importKey(keydata)
        h = SHA.new()
        u_str = message.encode('utf-8')
        h.update(u_str)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(h)
        b64sing = b64encode(signature)
        return b64sing

    def make_md5_sign(self, message):
        m = hashlib.md5()
        m.update(message)
        m.update(self.app.config['ALI_KEY'])
        return m.hexdigest()

    def check_sign(self, message, sign):
        """
        验证自签名
        :param message:
        :param sign:
        :return:
        """
        sign = base64.b64decode(sign)
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(self.app.config['RSA_PUBLIC'])
        return rsa.verify(message, sign, pubkey)

    def check_ali_sign(self, message, sign):
        """
        验证ali签名
        :param message:
        :param sign:
        :return:
        """
        sign = b64decode(sign)
        res = False
        with open(self.app.config['RSA_ALIPAY_PUBLIC_PATH']) as publicfile:
                keydata = publicfile.read()
        key = RSA.importKey(keydata)
        h = SHA.new()
        u_str = message.encode('utf-8')
        h.update(u_str)
        verifier = PKCS1_v1_5.new(key)
        res = verifier.verify(h, sign)
        return res

    def make_payment_request(self, params_dict):
        """
        构造一个支付请求的信息，包含最终结果里面包含签名
        :param params_dict:
        :return:
        """
        # query_str = self.params_to_query(params_dict, quotes=True) #拼接签名字符串
        query_str = 'partner=\"2088321008674225\"&seller_id=\"523453004@qq.com\"&out_trade_no=\"1012115637-9930\"&subject=\"测试的商品\"&body=\"该测试商品的详细描述\"&total_fee=\"0.01\"&notify_url=\"http://notify.msp.hk/notify.htm\"&service=\"mobile.securitypay.pay\"&payment_type=\"1\"&_input_charset=\"utf-8\"&it_b_pay=\"30m\"&return_url=\"m.alipay.com\"'
        sign = self.make_sign(query_str) #生成签名
        sign = str(sign, encoding='utf-8')
        sign = urllib.parse.quote_plus(sign)
        res = "%s&sign=\"%s\"&sign_type=\"RSA\"" % (query_str, sign)
        return res

    def make_payment_request2(self, params_dict):
        """
        构造一个支付请求的信息，包含最终结果里面包含签名
        :param params_dict:
        :return:
        """
        query_str = self.params_to_query(params_dict, quotes=False) #拼接签名字符串]
        sign = self.make_sign3(query_str) #生成签名
        sign = str(sign, encoding='utf-8')
        sign = urllib.parse.quote_plus(sign)
        query = ""
        for key in sorted(params_dict.keys(), reverse=False):
            value = params_dict[key]
            query += str(key) + "=" + urllib.parse.quote_plus(value.encode('utf-8')) + "&"
        query = query[0:-1]
        res = "%s&sign=%s" % (query, sign)
        return res

    def verify_alipay_request_sign(self, params_dict):
        """
        验证阿里支付回调接口签名
        :param params_dict: 阿里回调的参数列表
        :return:True or False
        """
        sign = params_dict['sign']
        params = self.params_filter(params_dict)
        message = self.params_to_query(params, quotes=False, reverse=False)
        check_res = self.check_ali_sign(message, sign)
        return check_res

    def verify_from_gateway(self, params_dict):
        """
        从阿里网管验证请求是否正确
        :param params_dict:
        :return:
        """
        ali_gateway_url = "https://mapi.alipay.com/gateway.do?service=notify_verify&partner=%(partner)d&notify_id=%(notify_id)s"
        notify_id = params_dict["notify_id"]
        partner = self.app.config['ALI_PARTNER_ID']
        ali_gateway_url = ali_gateway_url % {"partner": partner, "notify_id": notify_id}
        res = requests.get(ali_gateway_url)
        #    res_dict = encoder.XML2Dict.parse(res.text)
        if res.text == "true":
            return True
        return False

    def query_trade_status(self, params_dict):
        """
        从阿里网关查询订单状态
        :param params_dict:
        :return:
        """
        ali_gateway_url = "https://openapi.alipay.com/gateway.do"
        message = self.params_to_query(params_dict, quotes=False, reverse=False)
        sign = self.make_sign3(message) #生成签名
        sign = str(sign, encoding='utf-8')
        sign = urllib.parse.quote_plus(sign)
        query = ""
        for key in sorted(params_dict.keys(), reverse=False):
            value = params_dict[key]
            query += str(key) + "=" + urllib.parse.quote_plus(value.encode('utf-8')) + "&"
        query = query[0:-1]
        res = "%s&sign=%s" % (query, sign)
        ali_gateway_url = ali_gateway_url + '?' + res
        res = requests.get(ali_gateway_url)
        res_dict = json.loads(res.text)
        if res_dict['alipay_trade_query_response']['code'] != '10000':
            return False
        if res_dict['alipay_trade_query_response']['trade_status'] == 'TRADE_SUCCESS'\
                or res_dict['alipay_trade_query_response']['trade_status'] == 'TRADE_FINISHED':
            return True
        return False

    """
    构造一个支付请求
    """
    def make_payment_info(self, out_trade_no=None, subject=None, total_fee=None, body=None):
        order_info = {
            "partner": "%s" % (self.app.config['ALI_PARTNER_ID']),
            "service": "mobile.securitypay.pay",
            "_input_charset": "utf-8",
            "notify_url": "%s" % (self.app.config['ALI_NOTIFY_URL']),
            "out_trade_no": None,
            "paymnet_type": "1",
            "subject": None,
            "seller_id": "%s" % (self.app.config['ALI_ACCOUNT']),
            "total_fee": 0,
            "body": None
        }
        order_info["out_trade_no"] = "%s" % (out_trade_no)
        order_info["subject"] = "%s" % (subject)
        if total_fee <= 0.0:
            total_fee = 0.01
        order_info["total_fee"] = "%s" % (total_fee)
        order_info["body"] = "%s" % (body)
        return order_info

    """
    构造一个支付请求
    """
    def make_payment_info2(self, out_trade_no=None, subject=None, total_fee=None, body=None):
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        order_info = {
            "app_id": "%s" % (self.app.config['ALI_APP_ID']),
            "method": "alipay.trade.app.pay",
            "charset": "utf-8",
            "notify_url": "%s" % (self.app.config['ALI_NOTIFY_URL']),
            "sign_type": "RSA",
            "paymnet_type": "1",
            "timestamp": time_str,
            "version": "1.0",
            "biz_content": "{\"timeout_express\":\"30m\",\"product_code\":\"QUICK_MSECURITY_PAY\",\"total_amount\":\"" + str(total_fee) + "\",\"subject\":\"" + subject + "\",\"body\":\"" + body + "\",\"out_trade_no\":\"" + out_trade_no + "\"}"
            # "biz_content": "{\"timeout_express\":\"30m\",\"product_code\":\"QUICK_MSECURITY_PAY\",\"total_amount\":\"0.01\",\"subject\":\"1\",\"body\":\"我是测试数据\",\"out_trade_no\":\"1010171747-8241\"}"
        }
        return order_info

    """
    构造一个查询请求
    """
    def make_trade_query_info(self, out_trade_no=None):
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        order_info = {
            "app_id": "%s" % (self.app.config['ALI_APP_ID']),
            "method": "alipay.trade.query",
            "charset": "utf-8",
            "sign_type": "RSA",
            "timestamp": time_str,
            "version": "1.0",
            "biz_content": "{\"out_trade_no\":\"" + out_trade_no + "\"}"
        }
        return order_info














