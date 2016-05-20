from flask import jsonify, json, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.helper import success_json
from herovii.models.base import db
from herovii.models.org.info import Info
from herovii.models.org.teaching_course import TeachingCourse
from herovii.models.org.teaching_course_enroll import TeachingCourseEnroll
from herovii.models.overseas.organization_to_university import OrganizationToUniversity
from herovii.service.org import dto_org_teaching_courses_paginate, get_teaching_course_by_id, \
    get_teaching_course_detail_by_id, get_teaching_course_enroll_by_id
from herovii.validator.forms import PagingForm, OrgTeachingCourseForm, UpdateOrgTeachingCourseForm, \
    OrgTeachingCourseEnrollForm

__author__ = 'yangchujie'

api = ApiBlueprint('org')


@api.route('/teaching_course', methods=['POST'])
# @auth.login_required
def create_org_teaching_course():
    form = OrgTeachingCourseForm.create_api_form()
    teaching_course = TeachingCourse()
    for key, value in form.body_data.items():
        setattr(teaching_course, key, value)
    with db.auto_commit():
        db.session.add(teaching_course)
        db.session.commit()
        is_overseas_org = Info.query.filter_by(id=teaching_course.organization_id, type=31).first()
        if is_overseas_org:
            org_to_university = OrganizationToUniversity()
            org_to_university.organization_id = teaching_course.organization_id
            org_to_university.university_id = form.body_data['university_id']
            org_to_university.teaching_course_id = teaching_course.id
            db.session.add(org_to_university)
    return jsonify(teaching_course), 201


@api.route('/teaching_course', methods=['PUT'])
@auth.login_required
def update_org_teaching_course():
    form = UpdateOrgTeachingCourseForm.create_api_form()
    teaching_course = TeachingCourse.query.filter_by(id=form.id.data).first_or_404()
    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(teaching_course, key, value)
        is_overseas_org = Info.query.filter_by(id=teaching_course.organization_id, type=31).first()
        if is_overseas_org:
            if form.body_data['university_id']:
                db.session.query(OrganizationToUniversity).filter(
                    OrganizationToUniversity.teaching_course_id == teaching_course.id) \
                    .update({'university': form.body_data['university_id']})
    return jsonify(teaching_course), 202


@api.route('/teaching_course/<int:cid>', methods=['DELETE'])
@auth.login_required
def delete_org_teaching_course(cid):
    TeachingCourse.query.filter_by(id=cid).update({'status': -1})
    return success_json(), 204


@api.route('/<int:oid>/teaching_course')
# @auth.login_required
def list_teaching_courses(oid):
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    except_id = request.args.get('except_id', 0)
    dto = dto_org_teaching_courses_paginate(oid, except_id, form.page.data, form.per_page.data)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps(dto)
    return json_obj, 200, headers


@api.route('/teaching_course/<int:cid>')
# @auth.login_required
def get_teaching_course(cid):
    course = get_teaching_course_by_id(cid)
    json_data = json.dumps(course)
    headers = {'Content-Type': 'application/json'}
    return json_data, 200, headers


@api.route('/teaching_course/<int:cid>/detail')
# @auth.login_required
def get_teaching_course_detail(cid):
    course = get_teaching_course_detail_by_id(cid)
    json_data = json.dumps(course)
    headers = {'Content-Type': 'application/json'}
    return json_data, 200, headers


@api.route('/teaching_course/<int:cid>/enroll')
# @auth.login_required
def get_teaching_course_enroll(cid):
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    total_count, enroll_list = get_teaching_course_enroll_by_id(cid, form.page.data, form.per_page.data)
    result = {
        "total_count": total_count,
        "data": enroll_list
    }
    json_data = json.dumps(result)
    headers = {'Content-Type': 'application/json'}
    return json_data, 200, headers


@api.route('/teaching_course/<int:cid>/enroll', methods=['POST'])
# @auth.login_required
def create_org_teaching_course_enroll(cid):
    form = OrgTeachingCourseEnrollForm.create_api_form()
    teaching_course_enroll = TeachingCourseEnroll()
    for key, value in form.body_data.items():
        setattr(teaching_course_enroll, key, value)
    with db.auto_commit():
        db.session.add(teaching_course_enroll)
        course = TeachingCourse.query.get(cid)
        count = int(course.already_registered) + 1
        db.session.query(TeachingCourse).filter(TeachingCourse.id == cid).update({'already_registered': count})
    return jsonify(teaching_course_enroll), 201
