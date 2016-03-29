# -*- coding: utf-8 -*-
from flask import json, request
from herovii.cache import cache
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.util import parse_page_args, make_cache_key
from herovii.service.information_flow import get_information_flow_banner_service, get_information_flow_content_service, \
    get_information_flow_content_type_service

__author__ = 'yangchujie'

api = ApiBlueprint('information_flow')


@api.route('/banner', methods=['GET'])
@cache.cached(timeout=120, key_prefix='information_banner')
# @auth.login_required
def get_information_banner():
    request_json = request.get_json(force=True, silent=True)
    page, per_page = parse_page_args(request_json)
    total_count, data_list = get_information_flow_banner_service(page, per_page)
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/content', methods=['GET'])
@cache.cached(timeout=120, key_prefix=make_cache_key)
def get_information_flow_content():
    request_json = request.get_json(force=True, silent=True)
    page, per_page = parse_page_args(request_json)
    if request_json is None or 'type' not in request_json.keys():
        information_type = 0
    else:
        information_type = request_json['type']
    #user_info = g.user
    #uid = user_info[0]
    uid = 110
    if 'type' in request.args:
        information_type = int(request.args.get('type'))
    total_count, data_list = get_information_flow_content_service(uid, information_type, page, per_page)
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/type', methods=['GET'])
#@auth.login_required
def get_information_flow_content_type():
    total_count, data_list = get_information_flow_content_type_service()
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers
