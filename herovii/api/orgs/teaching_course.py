from flask import jsonify, json, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.helper import success_json
from herovii.models.base import db
from herovii.models.org.teaching_course import TeachingCourse
from herovii.service.org import get_course_by_id, dto_org_teaching_courses_paginate, get_teaching_course_by_id
from herovii.validator.forms import PagingForm, OrgTeachingCourseForm, UpdateOrgTeachingCourseForm

__author__ = 'yangchujie'

api = ApiBlueprint('org')


@api.route('/teaching_course', methods=['POST'])
@auth.login_required
def create_org_teaching_course():
    form = OrgTeachingCourseForm.create_api_form()
    teaching_course = TeachingCourse()
    for key, value in form.body_data.items():
        setattr(teaching_course, key, value)
    with db.auto_commit():
        db.session.add(teaching_course)
    return jsonify(teaching_course), 201


@api.route('/teaching_course', methods=['PUT'])
@auth.login_required
def update_org_teaching_course():
    form = UpdateOrgTeachingCourseForm.create_api_form()
    teaching_course = TeachingCourse.query.filter_by(id=form.id.data).first_or_404()
    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(teaching_course, key, value)
    return jsonify(teaching_course), 202


@api.route('/teaching_course/<int:cid>', methods=['DELETE'])
@auth.login_required
def delete_org_teaching_course(cid):
    TeachingCourse.query.filter_by(id=cid).update({'status': -1})
    return success_json(), 204


@api.route('/<int:oid>/teaching_course')
@auth.login_required
def list_teaching_courses(oid):
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    dto = dto_org_teaching_courses_paginate(oid, form.page.data, form.per_page.data)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps(dto)
    return json_obj, 200, headers


@api.route('/teaching_course/<int:cid>')
@auth.login_required
def get_teaching_course(cid):
    course = get_teaching_course_by_id(cid)
    json_data = json.dumps(course)
    headers = {'Content-Type': 'application/json'}
    return json_data, 200, headers
