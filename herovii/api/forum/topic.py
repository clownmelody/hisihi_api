# -*- coding: utf-8 -*-
import json
from flask import request
from herovii.libs.bpbase import ApiBlueprint
from herovii.service.forum import get_forum_hot_topic_list_service, get_forum_common_topic_list_service
from herovii.validator.forms import PagingForm

__author__ = 'yangchujie'


api = ApiBlueprint('topic')


@api.route('/hot', methods=['GET'])
def get_forum_hot_topic_list():
    total_count, data_list = get_forum_hot_topic_list_service()
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/common', methods=['GET'])
def get_forum_common_topic_list():
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    total_count, data_list = get_forum_common_topic_list_service(page, per_page)
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers
