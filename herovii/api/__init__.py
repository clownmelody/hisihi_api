# -*- coding: utf-8 -*-

import re

from flask import Blueprint

from herovii.api import user, token, sms, online, pk, test, mall, news, file, link, information_flow, follow
from herovii.api.im import im
from herovii.api.orgs import lecture, admin, course, enroll, info, news, resource, stats, student,\
    team, info, tag, classmate, feedback, video, teaching_course, overseas_study

from herovii.api import tags

__author__ = 'Whispers'


VERSION_URL = re.compile(r'^/api/\d/')
VERSION_ACCEPT = re.compile(r'application/vnd\.zerqu\+json;\s+version=(\d)')
CURRENT_VERSION = '1'
bp_v1 = Blueprint('v1', __name__)


# class ApiVersionMiddleware(object):
#     def __init__(self, app):
#         self.app = app
#
#     def __call__(self, environ, start_response):
#         path = environ.get('PATH_INFO')
#         if not path.startswith('/api/'):
#             return self.app(environ, start_response)
#         if VERSION_URL.match(path):
#             return self.app(environ, start_response)
#
#         # 修改url，强行在其中加入版本号
#         version = find_version(environ)
#
#         # environ['PATH_INFO'] 可以强制修改URL（修改的URL是没有匹配路由的URL，修改后才会同路由模板匹配
#         environ['PATH_INFO'] = path.replace('/api/', '/api/%s/' % version)
#         return self.app(environ, start_response)

class ApiVersionMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        version = environ.get('HTTP_VERSION')
        if not version:
            return self.app(environ, start_response)

        # # 修改url，强行在其中加入版本号
        # version = find_version(environ)

        # environ['PATH_INFO'] 可以强制修改URL（修改的URL是没有匹配路由的URL，修改后才会同路由模板匹配

        path = environ.get('PATH_INFO')

        environ['PATH_INFO'] = inject_version(path, version)
        return self.app(environ, start_response)


def inject_version(path, version):
    splits = path.split('/')
    splits.insert(3, version)
    path = '/'.join(splits)
    return path


def find_version(environ):
    accept = environ.get('HTTP_ACCEPT')
    if not accept:
        return CURRENT_VERSION
    rv = VERSION_ACCEPT.findall(accept)
    if rv:
        return rv[0]
    return CURRENT_VERSION


def init_api(app):
    app.wsgi_app = ApiVersionMiddleware(app.wsgi_app)
    reg_v1_bp(app)


def reg_v1_bp(app):
    user.api.register(bp_v1)
    online.api.register(bp_v1)
    pk.api.register(bp_v1)
    sms.api.register(bp_v1)
    test.api.register(bp_v1)
    token.api.register(bp_v1)
    mall.api.register(bp_v1)
    news.api.register(bp_v1)
    file.api.register(bp_v1)
    tags.api.register(bp_v1)
    link.api.register(bp_v1)
    follow.api.register(bp_v1)

    lecture.api.register(bp_v1)
    admin.api.register(bp_v1)
    course.api.register(bp_v1)
    enroll.api.register(bp_v1)
    info.api.register(bp_v1)
    news.api.register(bp_v1)
    resource.api.register(bp_v1)
    stats.api.register(bp_v1)
    student.api.register(bp_v1)
    tag.api.register(bp_v1)
    classmate.api.register(bp_v1)
    im.api.register(bp_v1)
    video.api.register(bp_v1)
    information_flow.api.register(bp_v1)

    feedback.api.register(bp_v1)
    teaching_course.api.register(bp_v1)
    overseas_study.api.register(bp_v1)

    app.register_blueprint(bp_v1, url_prefix='/v1')


