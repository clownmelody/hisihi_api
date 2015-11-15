__author__ = 'bliss'

from urllib import request as httpreq
from http.client import HTTPSConnection, HTTPResponse
from flask import json


class Httper(object):
    def get(self, url):
        return httpreq.urlopen(url)
        # with httpreq.urlopen(url) as f:
        #     data = f.read()
        #     print('Status:', f.status, f.reason)
        #     for k, v in f.getheaders():
        #         print('%s: %s' % (k, v))
        #     print('Data:', data.decode('utf-8'))
        # return f

    def post(self, host, url, data, headers=None):
        tmp_data = json.dumps(data)
        tmp_data = tmp_data.encode(encoding='utf-8')
        # req = httpreq.Request(url=url,
        #                       data=tmp_data, method='POST')
        # if headers is not None:
        #     req.headers = headers
        con = HTTPSConnection(host)
        con.request("POST", url, body=tmp_data, headers=headers)
        r = con.getresponse()
        # res = r.read()
        return r


class BMOB(Httper):
    # 短信服务商参数配置
    APP_ID = '8bee8ad5acaaa664f2f644c9e3a37c2e'
    API_KEY = '62060704177b04ee83d1bbc3778d5051'
    URI_SMS_CODE = r'https://api.bmob.cn/1/requestSmsCode'
    URI_VERIFY_SMS_CODE = r'https://api.bmob.cn/1/verifySmsCode/'
    API_HOST = "api.bmob.cn"
    header_dic = {'X-Bmob-Application-Id': APP_ID,
                  'X-Bmob-REST-API-Key': API_KEY,
                  'Content-Type': 'application/json'}

    def send_sms_code(self, phone_number):
        post_data = {'mobilePhoneNumber': phone_number}
        response = self.post(BMOB.API_HOST, BMOB.URI_SMS_CODE, post_data, BMOB.header_dic)
        return response.status, response.read()

    def verify_sms_code(self, phone_number, code):
        post_data = {'mobilePhoneNumber': phone_number}
        uri = BMOB.URI_VERIFY_SMS_CODE+code
        response = self.post(BMOB.API_HOST, uri, post_data, BMOB.header_dic)
        return response.status, response.read()


