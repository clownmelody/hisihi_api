# -*- coding: utf-8 -*-
from io import BytesIO
import qrcode
from herovii.libs.util import get_timestamp_with_random, year_month_day

__author__ = 'bliss'

import hashlib
import datetime,  random
from flask import request, current_app
from .enums import MobileRaceEnum
from .error_code import Successful


def get_url_no_param():
    full_path = str(request.full_path)
    q_index = full_path.find('?')
    full_path = full_path[0:q_index]

    return full_path


def android_ipad_iphone(http_user_agent):

    if 'iPhone' in http_user_agent:
        return MobileRaceEnum.iphone

    if 'iPad' in http_user_agent:
        return MobileRaceEnum.ipad

    if 'Android' in http_user_agent:
        return MobileRaceEnum.android

    return MobileRaceEnum.other


def success_json(code=None, msg=None, error_code=None):
    url = request.method+'  ' + get_url_no_param()
    return Successful(url, code, msg, error_code).get_json()


def dict_to_url_param(params_dict):
    m = map(lambda k: (k[0]+'='+str(k[1])+'&'), params_dict.items())
    url_params = '?'+''.join(m)
    url_params = url_params[:-1]
    return url_params


def check_md5_password(password, raw):
    """原始密码同md5加密的密码进行校验"""
    if not password:
        return False
    md5_password = secret_password(raw)
    if md5_password == password:
        return True
    else:
        return False


def secret_password(raw):
    """适用于UserCSU的密码加密算法"""
    salt = current_app.config['USER_PSW_SALT']
    sha1 = hashlib.sha1()
    sha1.update(raw.encode('utf-8'))
    sha1_psw = sha1.hexdigest()

    md5_raw = sha1_psw + salt
    m = hashlib.md5()
    m.update(md5_raw.encode('utf-8'))
    password = m.hexdigest()

    return password


def make_an_bizid():
    """生成一个微秒级别的时间字符串，并附带一个100到999之间的随机数"""
    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    bizid = time_str + str(random.randint(100, 999))
    return bizid


def allowed_uploaded_file_type(filename):
    filename = filename.lower()
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_FILE_EXTENSIONS']


def get_oss_file_url(extension):
    random_name = get_timestamp_with_random() + '.' + extension
    object_url = year_month_day() + '/' + random_name
    return object_url


def make_a_qrcode(uri):
    """生成一张二维码,返回一组bytes"""
    qr = qrcode.QRCode(
                        version=2,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=1
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image()
    png_bytes = BytesIO()
    img.save(png_bytes, 'png')
    return png_bytes


def is_first_party_cms():
    """是否是第一方CMS"""
    remote_addr = request.remote_addr
    if remote_addr == '115.29.44.35':
        return True
    else:
        return False


def get_full_oss_url(object_url, cdn=False, bucket_config='ALI_OSS_ORG_BUCKET_NAME'):
    if not object_url:
        return None
    if object_url.startswith('http://'):
        return object_url
    if cdn:
        host = current_app.config['ALI_OSS_CDN_HOST']
        full_oss_url = 'http://' + host + '/' + object_url
    else:
        host = current_app.config['ALI_OSS_HOST']
        bucket = current_app.config[bucket_config]
        full_oss_url = 'http://'+bucket + '.' + host + '/' + object_url

    return full_oss_url


def make_a_coupon_code(uid):
    """
    生成优惠码
    :param uid:
    :return:
    """
    uid_list = list(str(uid))
    uid_len = len(uid_list)
    #08开头，标识为优惠码
    coupon_code = ['0', '8']
    if uid_len < 7:
        for i in range(0, 7):
            if i < (7 - uid_len):
                coupon_code.append('0')
            else:
                num = int(uid_list[i - (7 - uid_len)]) * 3 + 6
                num_list = list(str(num))
                coupon_code.append(num_list[len(num_list) - 1])
    else:
        for i in range(0, 7):
            num = int(uid_list[i + uid_len - 7]) * 3 + 6
            num_list = list(str(num))
            coupon_code.append(num_list[len(num_list) - 1])
    for i in range(0, 7):
        r = random.randint(0, 9)
        coupon_code.append(str(int(r)))
    coupon_code_str = ''.join(coupon_code)
    return coupon_code_str


