import json

from flask import jsonify
from flask.globals import request

from herovii import db
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import ParamException, NotFound
from herovii.libs.helper import success_json
from herovii.libs.util import validate_int_arguments, validate_date_arguments
from herovii.models.org.classmate import Classmate
from herovii.models.org.student_class import StudentClass
from herovii.service.org import get_class_sign_in_detail_by_date, get_org_class_all_students_service, \
    get_org_all_class_service, get_org_enroll_student_service, get_org_class_info_service, join_org_class_service, \
    quit_org_class_service
from herovii.validator.forms import PagingForm, StudentClassForm, StudentClassUpdateForm, ClassmateJoinForm

__author__ = 'bliss'


api = ApiBlueprint('org')


@api.route('/<int:oid>/class/<int:cid>/sign-in/<date>/detail', methods=['GET'])
def get_org_class_sign_in_detail_by_data(oid, cid, date):
    """获取签到情况，按班级分类
       oid : 机构id号
       date: 日期 2015-12-10
       cid: 班级号
    """
    # Todo: @杨楚杰
    if not validate_int_arguments(oid):
        raise ParamException(error='organization id arguments is empty')
    if not validate_int_arguments(cid):
        raise ParamException(error='class id arguments is empty')
    date = validate_date_arguments(date)
    if not date:
        raise ParamException(error='date arguments exception')
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    data, total_count, sign_in_count, unsign_in_count = get_class_sign_in_detail_by_date(oid, cid, date, page, per_page)
    result = {
        "data": data,
        "total_count": total_count,
        "sign_in_count": sign_in_count,
        "unsign_in_count": unsign_in_count
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/<int:oid>/class/<int:cid>/students', methods=['GET'])
# @auth.login_required
# 获取班级下所有学生列表
def get_org_class_all_students(oid, cid):
    if not validate_int_arguments(oid):
        raise ParamException(error='organization id arguments is empty')
    if not validate_int_arguments(cid):
        raise ParamException(error='class id arguments is empty')
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    data, total_count = get_org_class_all_students_service(oid, cid, page, per_page)
    result = {
        "data": data,
        "total_count": total_count
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/<int:oid>/class', methods=['GET'])
@auth.login_required
def get_org_all_class(oid):
    if not validate_int_arguments(oid):
        raise ParamException(error='organization id arguments is empty')
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    data, total_count = get_org_all_class_service(oid, page, per_page)
    result = {
        "data": data,
        "total_count": total_count
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/<int:oid>/enroll/student', methods=['GET'])
@auth.login_required
def get_org_enroll_student(oid, name=None):
    if not validate_int_arguments(oid):
        raise ParamException(error='organization id arguments is empty')
    args = request.args.to_dict()
    if args.get('name'):
        name = args['name']
    data, total_count = get_org_enroll_student_service(oid, name)
    result = {
        "data": data,
        "total_count": total_count
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/class/info', methods=['POST'])
@auth.login_required
def create_org_class_info():
    form = StudentClassForm.create_api_form()
    post_data = form.body_data
    student_class = StudentClass(**post_data)
    with db.auto_commit():
        db.session.add(student_class)
    return jsonify(student_class), 201


@api.route('/class/info', methods=['PUT'])
@auth.login_required
def update_org_class_info():
    form = StudentClassUpdateForm.create_api_form()
    class_id = form.id.data
    class_info = StudentClass.query.get(class_id)
    if not class_info:
        raise NotFound(error='student_class not found')
    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(class_info, key, value)
    return jsonify(class_info), 202


@api.route('/class/<int:cid>/info', methods=['GET'])
@auth.login_required
def get_org_class_info(cid):
    if not validate_int_arguments(cid):
        raise ParamException(error='class id arguments is empty')
    data = get_org_class_info_service(cid)
    headers = {'Content-Type': 'application/json'}
    return jsonify(data), 200, headers


@api.route('/class/<int:cid>', methods=['DELETE'])
@auth.login_required
def delete_org_class_info(cid):
    if not validate_int_arguments(cid):
        raise ParamException(error='class id arguments is empty')
    with db.auto_commit():
        count = db.session.query(StudentClass).filter_by(id=cid).delete()
        db.session.query(Classmate).filter_by(class_id=cid).delete()
    msg = str(count) + ' class has been deleted'
    return success_json(msg=msg), 202


@api.route('/class/join', methods=['POST'])
@auth.login_required
def join_org_class():
    form = ClassmateJoinForm.create_api_form()
    uids = form.uids.data
    cid = form.cid.data
    msg = join_org_class_service(cid, uids)
    headers = {'Content-Type': 'application/json'}
    return success_json(msg=msg), 201, headers


@api.route('/class/quit', methods=['DELETE'])
@auth.login_required
def quit_org_class():
    form = ClassmateJoinForm.create_api_form()
    uids = form.uids.data
    cid = form.cid.data
    count = quit_org_class_service(cid, uids)
    msg = str(count) + ' students has been removed'
    headers = {'Content-Type': 'application/json'}
    return success_json(msg=msg), 202, headers
