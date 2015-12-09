from flask import jsonify, json, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.helper import success_json
from herovii.models.base import db
from herovii.models.org.course import Course
from herovii.service.org import dto_org_courses_paginate, get_course_by_id
from herovii.validator.forms import PagingForm, OrgCourseForm, OrgCourseUpdateForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/course', methods=['POST'])
@auth.login_required
def create_org_course():
    form = OrgCourseForm.create_api_form()
    course = Course()
    for key, value in form.body_data.items():
        setattr(course, key, value)
    with db.auto_commit():
        db.session.add(course)
    return jsonify(course), 201


@api.route('/course', methods=['PUT'])
@auth.login_required
def update_org_course():
    form = OrgCourseUpdateForm.create_api_form()
    course = Course.query.filter_by(id=form.id.data).first_or_404()
    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(course, key, value)
    return jsonify(course), 202


@api.route('/course/<int:cid>', methods=['DELETE'])
@auth.login_required
def delete_org_course(cid):
    Course.query.filter_by(id=cid).delete()
    return success_json(), 202


@api.route('/<int:oid>/courses')
# @auth.login_required
def list_courses(oid):
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    dto = dto_org_courses_paginate(oid, form.page.data, form.per_page.data)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps(dto)
    return json_obj, 200, headers


@api.route('/course/<int:cid>')
@auth.login_required
def get_course(cid):
    course = get_course_by_id(cid)
    json_data = json.dumps(course)
    headers = {'Content-Type': 'application/json'}
    return json_data, 200, headers
