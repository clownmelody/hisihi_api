__author__ = 'bliss'

from urllib import request as httpreq
from http.client import HTTPSConnection, HTTPResponse
from flask import json


class Httper(object):
    def get(self, url):
        req = httpreq.Request(url, method='GET')
        r = httpreq.urlopen(req)
        print(r)

    def post(self, host,url, data, headers=None):
        tmp_data = json.dumps(data)
        tmp_data = tmp_data.encode(encoding='utf-8')
        # req = httpreq.Request(url=url,
        #                       data=tmp_data, method='POST')
        # if headers is not None:
        #     req.headers = headers
        con = HTTPSConnection(host)
        con.request("POST", url, body=tmp_data, headers=headers)
        r = con.getresponse()
        res = r.read()
        return  res


class BMOB(Httper):
    # 短信服务商参数配置
    APP_ID = '8bee8ad5acaaa664f2f644c9e3a37c2e'
    API_KEY = '62060704177b04ee83d1bbc3778d5051'
    API_SMS_CODE = r'https://api.bmob.cn/1/requestSmsCode'
    API_HOST = "api.bmob.cn"

    def send_verify_sms(self, phone_number):
        header_dic = {'X-Bmob-Application-Id': BMOB.APP_ID,
                      'X-Bmob-REST-API-Key': BMOB.API_KEY,
                      'Content-Type': 'application/json'}
        post_data = {'mobilePhoneNumber': phone_number}
        response = self.post(BMOB.API_HOST, BMOB.API_SMS_CODE, post_data, header_dic)
        status = response.status
