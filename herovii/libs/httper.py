__author__ = 'bliss'

from urllib import request as httpreq
import http.client
from urllib.error import HTTPError
from flask import json


class Httper(object):
    def get(self, url):
        req = httpreq.Request(url, method='GET')
        r = httpreq.urlopen(req)
        print(r)

    def post(self, url, data, headers=None):
        tmp_data = json.dumps(data)
        tmp_data = tmp_data.encode(encoding='utf-8')
        req = httpreq.Request(url=url,
                              data=tmp_data, method='POST')
        if headers is not None:
            req.headers = headers

        try:
            r = httpreq.urlopen(req, timeout=120)
        except HTTPError as e:
            s = e

        # r = request.urlopen('http://sina.com')
        rlt = r.read()
        print(rlt)
        return r


class BMOB(Httper):
    # 短信服务商参数配置
    APP_ID = '8bee8ad5acaaa664f2f644c9e3a37c2e'
    API_KEY = '62060704177b04ee83d1bbc3778d5051111'
    API_SMS_CODE = r'https://api.bmob.cn/1/requestSmsCode'

    def send_verify_sms(self, phone_number):
        header_dic = {'X-Bmob-Application-Id': BMOB.APP_ID,
                      'X-Bmob-REST-API-Key': BMOB.API_KEY,
                      'Content-Type': 'application/json'}
        post_data = {'mobilePhoneNumber': phone_number}
        r = self.post(BMOB.API_SMS_CODE, post_data, header_dic)
        print(r)
