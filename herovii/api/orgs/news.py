from flask import json
from flask.globals import request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.service.news import get_news_dto_paginate
from herovii.validator.forms import PagingForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/news', methods=['GET'])
# @auth.login_required
def list_news():
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    news = get_news_dto_paginate(int(form.page.data), int(form.per_page.data))
    headers = {'Content-Type': 'application/json'}
    return json.dumps(news), 200, headers

