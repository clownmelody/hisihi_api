# -*- coding: utf-8 -*-
import hmac, hashlib
from random import Random
import time

__author__ = 'yangchujie'


# LeanCloud 签名算法
def sign(msg, k):
    return hmac.new(bytes(k, 'utf-8'), bytes(msg, 'utf-8'), hashlib.sha1).hexdigest()


# 获取当前时间戳
def get_timestamp():
    return str(time.time())


# 生成随机字符串
def get_nonce(nonce_length=8):
    nonce = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(nonce_length):
        nonce += chars[random.randint(0, length)]
    return nonce
