__author__ = 'bliss'

# coding: utf-8

import datetime

# App Param Defination

# 在返回结果中显示错误的具体内容，默认True
SHOW_DETAIL_ERROR = True

SITE_NAME = 'HiWebAPI'
SITE_DESCRIPTION = 'Welcome to HiWebAPI'
SITE_YEAR = datetime.date.today().year

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:19851118@101.200.236.82/org'
SQLALCHEMY_BINDS = {
    'test': 'sqlite:///tmp/test1.db',
    'online': 'mysql+cymysql://root:19851118@101.200.236.82/online'
}
SECRET_KEY = '\xeb\xb3\x1bx\x10o\xa4\xb8\x0b\x05\xf5\xb6k\x0bNX\x1f\x86\\\xb9\x1c*\x1d\x95'

APP_LINKS = [{'name': 'About', 'url': '/c/about'}]
APP_LOGIN = []
APP_HEADER = ''
APP_FOOTER = ''

OAUTH2_CACHE_TYPE = 'redis'
OAUTH2_CACHE_REDIS_DB = 1
