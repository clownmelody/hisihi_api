import os, sys

__author__ = 'bliss'

from flask import request, redirect

from herovii.libs.bpbase import ApiBlueprint
from herovii.api.token import auth

api = ApiBlueprint('test')


@api.route('/get', methods=['GET'])
def test_javascript_http():
    p = request.args.get('name')
    return p, 200


@api.route('/client-ip', methods=['GET'])
def test_client_ip():
    r = request.remote_addr
    return r, 200


@api.route('/dev')
def test_new_dev():
    a = 1/0
    return 'dev is ok', 200


@api.route('/redirect')
def test_redirect():
    return redirect('http://sina.com')


@api.route('/log')
def test_log():
    import logging
    formatter = logging.Formatter(
        '[%(asctime)s %(levelname)s %(funcName)s %(filename)s:%(lineno)d]: %(message)s'
    )

    file_handler = logging.FileHandler('log.txt')
    path = os.path.abspath('.')
    path1 = os.getcwd()

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    logger = logging.getLogger('test')
    logger.addHandler(file_handler)
    logger.warning(path)
    logger.warning(path1)
    path2 = cur_file_dir()
    logging.warning(path2)
    return 'success', 200


@api.route('/download+1', methods=['PUT'])
def downloads_plus_1():
    pass


@api.route('/error-log')
def test_error_log():
    i = 2/0
    return i, 200


@api.route('/auth')
@auth.login_required
def test_auth():
    return 'success', 200


def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)


