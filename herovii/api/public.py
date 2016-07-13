# -*- coding: utf-8 -*-
from flask import json, request
from herovii import db
from herovii.libs.bpbase import ApiBlueprint
from herovii.models.recomend_majors import RecomendMajors

__author__ = 'yangchujie'

api = ApiBlueprint('public')


@api.route('/recomend_majors', methods=['GET'])
def get_recomend_majors():
    _list = db.session.query(RecomendMajors) \
        .filter(RecomendMajors.status == 1) \
        .order_by(RecomendMajors.sort.desc()) \
        .all()
    total_count = len(_list)
    data_list = []
    for major in _list:
        obj = {
            "name": major.name,
            "sort": major.sort
        }
        data_list.append(obj)
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers
