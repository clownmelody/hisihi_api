# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask import json

from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.helper import success_json
from herovii.models.yellowpages.pageclass import Category
from herovii.models.yellowpages.yellowpages import Yellow
from herovii.service.yellow import get_yellow_pages_list, get_recommend_sites
from herovii.validator.forms import PagingForm, YellowPagesForm, CategoryForm
from herovii.models.base import db

__author__ = 'melody'

api = ApiBlueprint('link')


@api.route('/yellow_pages', methods=['GET'])
def show_list():
    # 返回导航网址和分类列表
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    yellow_pages = get_yellow_pages_list(int(form.page.data), int(form.per_page.data))
    headers = {'Content-Type': 'application/json'}
    return json.dumps(yellow_pages), 200, headers


@api.route('/yellow_pages/recommend', methods=['GET'])
def show_recommend():
    # 返回推荐网址
    recommend_pages = get_recommend_sites()
    headers = {'Content-Type': 'application/json'}
    return json.dumps(recommend_pages), 200, headers


@api.route('/yellow_page', methods=['POST'])
def create_site_info():
    # 创建网址信息
    form = YellowPagesForm.create_api_form()
    yellow = Yellow()
    with db.auto_commit():
        yellow.id = form.id.data
        yellow.web_name = form.web_name.data
        yellow.url = form.url.data
        yellow.icon_url = form.icon_url.data
        yellow.class_id = form.class_id.data
        yellow.state = form.state.data
        yellow.real_score = form.real_score.data
        yellow.fake_score = form.fake_score.data
        db.session.add(yellow)
    return jsonify(yellow), 201


@api.route('/yellow_page', methods=['PUT'])
def update_site_info(gid):
    # 更新和删除网址信息
    with db.auto_commit():
        count = db.session.query(Yellow).\
                        filter_by(id=gid).delete()
    msg = str(count) + ' site has been deleted'
    return success_json(msg=msg), 202


@api.route('/category', method=['POST'])
def create_category_info():
    # 创建类别信息
    form = CategoryForm.create_api_form()
    category = Category()
    with db.auto_commit():
        category.id = form.id.data
        category.category_name = form.category_name.data
        category.icon_url = form.icon_url.data
        db.session.add(category)
    return jsonify(category), 201


@api.route('/category', method=['PUT'])
def update_site_info(gid):
    # 更新和删除类别信息
    with db.auto_commit():
        count = db.session.query(Category).\
                        filter_by(id=gid).delete()
    msg = str(count) + ' site has been deleted'
    return success_json(msg=msg), 202
