from flask import jsonify, g, json, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import IllegalOperation, OrgNotFound, UnknownError
from herovii.libs.httper import BMOB
from herovii.libs.helper import success_json
from herovii.models.base import db
from herovii.models.org import org_course
from herovii.models.org.org_course import OrgCourse
from herovii.models.org.org_info import OrgInfo
from herovii.models.org.teacher_group import TeacherGroup
from herovii.models.org.teacher_group_realation import TeacherGroupRealation
from herovii.service import account
from herovii.service.org import create_org_info, get_org_teachers_by_group, get_org_courses, dto_org_courses_paginate, \
    get_course_by_id
from herovii.service.news import get_news_dto_paginate
from herovii.validator.forms import OrgForm, OrgUpdateForm, TeacherGroupForm, RegisterByMobileForm, PagingForm, \
    OrgCourseForm, OrgCourseUpdateForm
from herovii.service.user_org import register_by_mobile

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/admin', methods=['POST'])
def create_org_admin():
    """ 添加一个机构用户
    调用此接口需要先调用'/v1/sms/verify' 接口，以获得短信验证码
    :POST:
        {'phone_number':'18699998888', 'sms_code':'876876', 'password':'password'}
    :return:
    """
    bmob = BMOB()
    form = RegisterByMobileForm.create_api_form()
    phone_number = form.mobile.data
    password = form.password.data
    sms_code = form.sms_code.data
    status, body = bmob.verify_sms_code(phone_number, sms_code)
    if status == 200:
        user = register_by_mobile(phone_number, password)
        return jsonify(user), 201
    else:
        j = json.loads(body)
        raise UnknownError(j['error'], error_code=None)


@api.route('/admin/password', methods=['PUT'])
def find_admin_password():
    """ 重置/找回密码
        调用此接口需要先调用'/v1/sms/verify' 接口，以获得短信验证码
    :PUT:
        {"phone_number":'18699998888', "sms_code":'876876', "password":'password'}
    :return:
    """
    bmob = BMOB()
    form = RegisterByMobileForm.create_api_form()
    mobile = form.phone_number.data
    password = form.password.data
    sms_code = form.sms_code.data
    status, body = bmob.verify_sms_code(mobile, sms_code)
    if status == 200:
        account.reset_password_by_mobile(mobile, password)
        return success_json(), 202
    else:
        j = json.loads(body)
        raise UnknownError(j['error'], error_code=None)


@api.route('/news', methods=['GET'])
@auth.login_required
def list_news():
    args = request.args
    form = PagingForm.create_api_form(**args)
    news = get_news_dto_paginate(int(form.page.data[0]), int(form.per_page.data[0]))
    headers = {'Content-Type': 'application/json'}
    return json.dumps(news), 200, headers


@api.route('/admin/<int:id>', methods=['GET'])
def get_org_admin(id):
    pass


@api.route('/admin/<int:id>', methods=['PUT'])
def update_org_admin(id):
    pass


@api.route('', methods=['POST'])
@auth.login_required
def create_org():
    form = OrgForm.create_api_form()
    post_data = form.body_data
    org = OrgInfo(**post_data)
    create_org_info(org)
    return jsonify(org), 201


@api.route('', methods=['PUT'])
@auth.login_required
def update_org():
    form = OrgUpdateForm().create_api_form()
    org_id = form.id.data
    org_info = OrgInfo.query.get(org_id)
    if not org_info:
        raise OrgNotFound()
    if org_info.uid != g.user[0]:
        raise IllegalOperation()

    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(org_info, key, value)
    return jsonify(org_info), 202


@api.route('/teacher/group', methods=['POST'])
@auth.login_required
def create_teacher_group():
    form = TeacherGroupForm.create_api_form()
    group = TeacherGroup()
    with db.auto_commit():
        group.organization_id = form.organization_id.data
        group.title = form.title.data
        db.session.add(group)
    return jsonify(group), 201


@api.route('/teacher/group/<int:gid>', methods=['Delete'])
@auth.login_required
def delete_teacher_group(gid):
    with db.auto_commit():
        count = db.session.query(TeacherGroup).\
                        filter_by(id=gid).delete()
        count1 = db.session.query(TeacherGroupRealation).filter_by(
            teacher_group_id=gid).delete()
    msg = str(count+count1) + ' groups has been deleted'
    return success_json(msg=msg), 202


@api.route('/teacher/<int:uid>/group/<int:g_id>/join', methods=['POST'])
@auth.login_required
def join_teacher_group(uid, g_id):
    t_g_realation = TeacherGroupRealation()
    t_g_realation.teacher_group_id = g_id
    t_g_realation.uid = uid
    with db.auto_commit():
        db.session.add(t_g_realation)
    return jsonify(t_g_realation)


@api.route('/teacher/<int:uid>/group/<int:gid>/join', methods=['DELETE'])
@auth.login_required
def retire_from_teacher_group(uid, gid):
    s = 1
    count = TeacherGroupRealation.query.filter(
        TeacherGroupRealation.uid == uid, TeacherGroupRealation.teacher_group_id == gid) \
        .delete()
    msg = count + 'teacher identity has been removed'
    return success_json(msg=msg), 202


@api.route('/<int:oid>/teachers', methods=['GET'])
@auth.login_required
def get_teachers_in_org(oid):
    teachers = get_org_teachers_by_group(oid)
    headers = {'Content-Type': 'application/json'}
    t = json.dumps(teachers)
    return t, 200, headers


@api.route('/<int:oid>', methods=['GET'])
@auth.login_required
def get_org(oid):
    org_info = OrgInfo.query.get(oid)
    if not org_info:
        raise OrgNotFound()
    if org_info.uid != g.user[0]:
        raise IllegalOperation()
    return jsonify(org_info), 200


@api.route('/course', methods=['POST'])
@auth.login_required
def create_org_course():
    form = OrgCourseForm.create_api_form()
    course = OrgCourse()
    for key, value in form.body_data.items():
        setattr(course, key, value)
    with db.auto_commit():
        db.session.add(course)
    return jsonify(course), 201


@api.route('/course', methods=['PUT'])
@auth.login_required
def update_org_course():
    form = OrgCourseUpdateForm.create_api_form()
    course = OrgCourse.query.filter_by(id=form.id.data).first_or_404()
    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(course, key, value)
    return jsonify(course), 202


@api.route('/course/<int:cid>', methods=['DELETE'])
@auth.login_required
def delete_org_course(cid):
    OrgCourse.query.filter_by(id=cid).delete()
    return success_json(), 202


@api.route('/<int:oid>/courses')
@auth.login_required
def list_courses(oid):
    args = request.args
    form = PagingForm.create_api_form(**args)
    dto = dto_org_courses_paginate(oid, form.page.data[0], form.per_page.data[0])
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps(dto)
    return json_obj, 200, headers


@api.route('/courses/<int:cid>')
@auth.login_required
def get_course(cid):
    course = get_course_by_id(cid)
    json_data = json.dumps(course)
    headers = {'Content-Type': 'application/json'}
    return json_data, 200, headers




