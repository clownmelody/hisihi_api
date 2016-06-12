# -*- coding: utf-8 -*-
import json
from herovii.libs.bpbase import ApiBlueprint
from herovii.service.forum import get_forum_topic_list_service

__author__ = 'yangchujie'


api = ApiBlueprint('topic')


@api.route('/hot', methods=['GET'])
def get_forum_hot_topic_list():
    total_count, data_list = get_forum_topic_list_service(is_hot=1)
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/common', methods=['GET'])
def get_forum_common_topic_list():
    total_count, data_list = get_forum_topic_list_service(is_hot=-1)
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers
