__author__ = 'bliss'

# coding: utf-8

import datetime


# 在返回结果中显示错误的具体内容，默认True
SHOW_DETAIL_ERROR = True

SITE_NAME = 'HiWebAPI'
SITE_DESCRIPTION = 'Welcome to HiWebAPI'
SITE_YEAR = datetime.date.today().year

APP_LINKS = [{'name': 'About', 'url': '/c/about'}]
APP_LOGIN = []
APP_HEADER = ''
APP_FOOTER = ''

OAUTH2_CACHE_TYPE = 'redis'
OAUTH2_CACHE_REDIS_DB = 1
