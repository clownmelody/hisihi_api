__author__ = 'bliss'

import  random


def generate_app():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(16):
        sa.append(random.choice(seed))

    salt = ''.join(sa)
    print(salt)


# oss = OssAPI(access_id='3uFZDrxg6fGKZq8P', is_security=True,
#              secret_access_key='LxsXIcp7ghkyqABJYIHYjmcsku1VOS')
#
# oss.put_object_from_string('hisihi-avator', 'mrl_test_aaaa', 'this is for test')