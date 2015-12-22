import datetime
import json
from flask import jsonify, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import IllegalOperation, ParamException, UpdateDBError
from herovii.libs.util import is_today, validate_int_arguments
from herovii.models.base import db
from herovii.models.org.student_class import StudentClass
from herovii.models.org.classmate import Classmate
from herovii.service.enroll import update_stu_graduation_status
from herovii.service.org import create_student_sign_in, get_org_student_profile_by_uid, \
    get_org_student_sign_in_history_by_uid, get_org_student_class_in, move_student_to
from herovii.validator.forms import StudentClassForm, StudentJoinForm, PagingForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/<int:oid>/student/<int:uid>/sign-in/<date>', methods=['POST'])
@auth.login_required
def student_sign_in(oid, uid, date):
    # init_classmate_mirror(oid, date)
    date_sign_in = datetime.datetime.strptime(date, '%Y-%m-%d')
    today = is_today(date_sign_in)

    if not today:
        raise IllegalOperation(error='date is not today')

    today_str = date_sign_in.strftime('%Y-%m-%d')
    sign_in = create_student_sign_in(oid, uid, today_str)
    return jsonify(sign_in), 201


@api.route('/<int:oid>/class/<int:cid>/sign-in')
def get_class_sign_in_detail(oid, cid):
    pass


@api.route('/student/class', methods=['POST'])
def create_student_class():
    form = StudentClassForm.create_api_form()
    s_class = StudentClass()
    s_class.organization_id = form.organization_id.data
    s_class.title = form.title.data

    # stats_class = StudentClassStats()
    with db.auto_commit():
        db.session.add(s_class)
    return jsonify(s_class), 201


@api.route('/student/class/join', methods=['POST'])
def move_student_to_class():
    form = StudentJoinForm.create_api_form()
    s_c_relation = Classmate()
    s_c_relation.uid = form.uid.data
    s_c_relation.student_class_id = form.student_class_id.data

    with db.auto_commit():
        db.session.add(s_c_relation)
    return jsonify(s_c_relation), 201


@api.route('/student/<int:uid>/class/<int:class_id>/move', methods=['PUT'])
def move_student_from_to(uid, class_id):
    """
    修改学生所属分组
    :param uid:学生id
    :param class_id:新分组id
    :return:
    """
    if not validate_int_arguments(uid):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    if not validate_int_arguments(class_id):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    res = move_student_to(uid, class_id)
    headers = {'Content-Type': 'application/json'}
    return jsonify(res), 202, headers


@api.route('/student/<int:uid>/profile', methods=['GET'])
@auth.login_required
def get_student_profile(uid):
    """获取学生资料
       uid: 学生id号
    """
    # Todo: @杨楚杰
    if not validate_int_arguments(uid):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    student = get_org_student_profile_by_uid(uid)
    headers = {'Content-Type': 'application/json'}
    student_json = jsonify(student)
    return student_json, 200, headers


@api.route('/student/<int:uid>/sign-in/history', methods=['GET'])
@auth.login_required
def get_student_sign_in_history(uid):
    """获取学生历史签到记录
       uid: 学生id号
    """
    # Todo: @杨楚杰
    if not validate_int_arguments(uid):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    total_count, sign_in_history = get_org_student_sign_in_history_by_uid(uid, page, per_page)
    headers = {'Content-Type': 'application/json'}
    result = {
        'sign_in_history': sign_in_history,
        'total_count': total_count
    }
    sign_in_history_json = json.dumps(result)
    return sign_in_history_json, 200, headers


@api.route('/student/<int:uid>/class/<int:oid>/in', methods=['GET'])
@auth.login_required
def get_student_class_in(uid, oid):
    """获取学生所在分组
       uid: 学生id号
    """
    if not validate_int_arguments(uid):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    if not validate_int_arguments(oid):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    class_in, class_total_count = get_org_student_class_in(uid, oid)
    headers = {'Content-Type': 'application/json'}
    result = {
        'class_list': class_in,
        'total_count': class_total_count
    }
    class_in_json = json.dumps(result)
    return class_in_json, 200, headers


@api.route('/student/<int:uid>/graduation/<int:oid>/status/<int:status>', methods=['PUT'])
@auth.login_required
def update_graduation(uid, oid, status):
    if not validate_int_arguments(uid):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    if not validate_int_arguments(oid):
        raise ParamException(error='the data to update is empty',
                             error_code=1001, code=200)
    if not validate_int_arguments(status):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    if status != 2 and status != 3:
        raise ParamException(error='the status is limited to be 2 or 3',
                             error_code=1001, code=200)
    res = update_stu_graduation_status(uid, oid, status)
    if res:
        headers = {'Content-Type': 'application/json'}
        return jsonify(res), 202, headers
    else:
        raise UpdateDBError()
