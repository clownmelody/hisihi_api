# -*- coding: utf-8 -*-
from flask import json, request
from herovii.cache import cache
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.util import parse_page_args, make_cache_key
from herovii.service.information_flow import get_information_flow_banner_service, get_information_flow_content_service, \
    get_information_flow_content_type_service, get_information_flow_content_service_v2_7

__author__ = 'yangchujie'

api = ApiBlueprint('information_flow')


@api.route('/banner', methods=['GET'])
@cache.cached(timeout=120, key_prefix='information_banner')
def get_information_banner():
    request_json = request.get_json(force=True, silent=True)
    page, per_page = parse_page_args(request_json)
    total_count, data_list = get_information_flow_banner_service(page, per_page, 2.6)
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/2.7/banner', methods=['GET'])
@cache.cached(timeout=120, key_prefix='information_banner_v2.7')
def get_information_banner_v2_7():
    request_json = request.get_json(force=True, silent=True)
    page, per_page = parse_page_args(request_json)
    total_count, data_list = get_information_flow_banner_service(page, per_page, 2.7)
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


@api.route('/2.7/content', methods=['GET'])
@cache.cached(timeout=120, key_prefix=make_cache_key)
def get_information_flow_content_v2_7():
    request_json = request.get_json(force=True, silent=True)
    page, per_page = parse_page_args(request_json)
    if request_json is None or 'type' not in request_json.keys():
        information_type = 0
    else:
        information_type = request_json['type']
    uid = 110
    if 'type' in request.args:
        information_type = int(request.args.get('type'))
    total_count, data_list = get_information_flow_content_service_v2_7(uid, information_type, page, per_page)
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/type', methods=['GET'])
def get_information_flow_content_type():
    total_count, data_list = get_information_flow_content_type_service()
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers
