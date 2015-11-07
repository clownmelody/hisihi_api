__author__ = 'bliss'

from flask import request
from herovii.libs.bpbase import ApiBlueprint

api = ApiBlueprint('test')


@api.route('/get', methods=['GET'])
def test_javascript_http():
    return 'hello', 200


@api.route('/client-ip', methods=['GET'])
def test_client_ip():
    r = request.remote_addr
    return r, 200


@api.route('/error-log')
def test_error_log():
    i = 2/0
    return i, 200

