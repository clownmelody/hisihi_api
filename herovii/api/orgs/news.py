from flask import json, jsonify
from flask.globals import request
from herovii import db
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.helper import success_json
from herovii.models.news.news_org import NewsOrg
from herovii.service.news import get_news_dto_paginate, get_news_org_by_id
from herovii.validator.forms import PagingForm, NewsForm, UpdateNewsForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/news', methods=['GET'])
@auth.login_required
def list_news():
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    news = get_news_dto_paginate(int(form.page.data), int(form.per_page.data))
    headers = {'Content-Type': 'application/json'}
    return json.dumps(news), 200, headers


@api.route('/news', methods=['POST'])
@auth.login_required
def add_news():
    form = NewsForm.create_api_form()
    news = NewsOrg()
    for key, value in form.body_data.items():
        setattr(news, key, value)
    with db.auto_commit():
        db.session.add(news)
    return jsonify(news), 201


@api.route('/news', methods=['PUT'])
@auth.login_required
def update_org_news():
    form = UpdateNewsForm.create_api_form()
    news = NewsOrg.query.filter_by(id=form.id.data).first_or_404()
    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(news, key, value)
    return jsonify(news), 202


@api.route('/news/<int:nid>', methods=['DELETE'])
@auth.login_required
def delete_org_news(nid):
    NewsOrg.query.filter_by(id=nid).update({'status': -1})
    return success_json(), 204


@api.route('/news/<int:nid>')
@auth.login_required
def get_news(nid):
    course = get_news_org_by_id(nid)
    json_data = json.dumps(course)
    headers = {'Content-Type': 'application/json'}
    return json_data, 200, headers


