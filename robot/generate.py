__author__ = 'bliss'

import  random


def generate_app():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(16):
        sa.append(random.choice(seed))

    salt = ''.join(sa)
    print(salt)
