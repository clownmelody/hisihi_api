# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask import json

from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.helper import success_json
from herovii.models.yellowpages.pageclass import Category
from herovii.models.yellowpages.yellowpages import Yellow
from herovii.service.yellow import get_yellow_pages_list, get_recommend_sites
from herovii.validator.forms import YellowPagesForm, CategoryForm, UpdateCategoryForm, UpdateYellowPagesForm
from herovii.models.base import db

__author__ = 'melody'

api = ApiBlueprint('link')


@api.route('/yellow_pages', methods=['GET'])
def show_list():
    # 返回导航网址和分类列表
    yellow_pages = get_yellow_pages_list()
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
    for key, value in form.body_data.items():
        setattr(yellow, key, value)
    with db.auto_commit():
        db.session.add(yellow)
    return jsonify(yellow), 201


@api.route('/yellow_page/<int:wid>', methods=['PUT'])
def update_site_info(wid):
    # 更新和删除网址信息

    form = UpdateYellowPagesForm.create_api_form()
    yellow = db.session.query(Yellow).filter_by(id=wid).first()
    for key, value in form.body_data.items():
        setattr(yellow, key, value)
    with db.auto_commit():
        db.session.commit()

    msg = ' site has been updated'

    return success_json(msg=msg), 202


@api.route('/category', methods=['POST'])
def create_category_info():
    # 创建类别信息
    form = CategoryForm.create_api_form()
    category = Category()

    for key, value in form.body_data.items():
        setattr(category, key, value)

    with db.auto_commit():
        db.session.add(category)
    return jsonify(category), 201


@api.route('/category/<int:cid>', methods=['PUT'])
def update_category_info(cid):
    # 更新和删除类别信息

    form = UpdateCategoryForm.create_api_form()
    category = db.session.query(Category).filter_by(id=cid).first()

    for key, value in form.body_data.items():
        setattr(category, key, value)

    with db.auto_commit():
        db.session.commit()

    msg = ' category has been updated'
    return success_json(msg=msg), 202
