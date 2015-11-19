from flask import json
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.service.news import  get_news_dto_paginate
from herovii.validator.forms import PagingForm

__author__ = 'bliss'

api = ApiBlueprint('news')


@api.route('/org', methods=['GET'])
@auth.login_required
def list_news():
    form = PagingForm.create_api_form(ignore_none=True)
    news = get_news_dto_paginate(form.page.data, form.count.data)
    headers = {'Content-Type': 'application/json'}
    return json.dumps(news), 200, headers


