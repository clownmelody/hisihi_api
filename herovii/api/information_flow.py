# -*- coding: utf-8 -*-
from flask import json, request
from herovii.libs.bpbase import ApiBlueprint
from herovii.service.information_flow import get_information_flow_banner_service
from herovii.validator.forms import PagingForm

__author__ = 'yangchujie'

api = ApiBlueprint('information_flow')


@api.route('/banner', methods=['GET'])
# @auth.login_required
def get_information_banner():
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    total_count, data_list = get_information_flow_banner_service(page, per_page)
    result = {
        'total_count': total_count,
        'data': data_list
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers
