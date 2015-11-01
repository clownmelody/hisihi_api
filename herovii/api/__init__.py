__author__ = 'Whispers'

import re
from flask import Blueprint, request
from herovii.api import user

VERSION_URL = re.compile(r'^/api/\d/')
VERSION_ACCEPT = re.compile(r'application/vnd\.zerqu\+json;\s+version=(\d)')
CURRENT_VERSION = '1'
bp = Blueprint('api', __name__)


class ApiVersionMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        if not path.startswith('/api/'):
            return self.app(environ, start_response)
        if VERSION_URL.match(path):
            return self.app(environ, start_response)

        # 修改url，强行在其中加入版本号
        version = find_version(environ)

        # environ['PATH_INFO'] 可以强制修改URL（修改的URL是没有匹配路由的URL，修改后才会同路由模板匹配
        environ['PATH_INFO'] = path.replace('/api/', '/api/%s/' % version)
        return self.app(environ, start_response)


def find_version(environ):
    accept = environ.get('HTTP_ACCEPT')
    if not accept:
        return CURRENT_VERSION
    rv = VERSION_ACCEPT.findall(accept)
    if rv:
        return rv[0]
    return CURRENT_VERSION


def init_app(app):
    # app.wsgi_app = ApiVersionMiddleware(app.wsgi_app)
    user.api.register(bp)

    # api 1.0版本 blueprint注册接口
    app.register_blueprint(bp, url_prefix='/v1')
