from flask import jsonify, json
from flask.globals import request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import ParamException

from herovii.libs.helper import success_json
from herovii.models.base import db

from herovii.models.org.teacher_group import TeacherGroup
from herovii.models.org.teacher_group_relation import TeacherGroupRelation

from herovii.service.org import get_org_teachers_by_group, search_lecture, get_org_teachers, set_lecturer_extend_info
from herovii.validator.forms import TeacherGroupForm, LectureJoinForm, PagingForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/lecture/group', methods=['POST'])
@auth.login_required
def create_teacher_group():
    form = TeacherGroupForm.create_api_form()
    group = TeacherGroup()
    with db.auto_commit():
        group.organization_id = form.organization_id.data
        group.title = form.title.data
        db.session.add(group)
    return jsonify(group), 201


@api.route('/lecture/group/<int:gid>', methods=['Delete'])
@auth.login_required
def delete_teacher_group(gid):
    with db.auto_commit():
        count = db.session.query(TeacherGroup).\
                        filter_by(id=gid).delete()
        db.session.query(TeacherGroupRelation).filter_by(
            teacher_group_id=gid).delete()
    msg = str(count) + ' groups has been deleted'
    return success_json(msg=msg), 202


@api.route('/lecture/group/join', methods=['POST'])
@auth.login_required
def join_teacher_group():
    form = LectureJoinForm.create_api_form()
    t_g_relation = TeacherGroupRelation()
    t_g_relation.teacher_group_id = form.teacher_group_id.data
    t_g_relation.uid = form.uid.data
    t_g_relation.organization_id = form.oid.data
    t_g_relation.group = 6
    set_lecturer_extend_info(t_g_relation.uid, t_g_relation.organization_id)
    with db.auto_commit():
        db.session.add(t_g_relation)
    return jsonify(t_g_relation), 201


@api.route('/lecture/<int:uid>/group/<int:gid>/quite', methods=['DELETE'])
@auth.login_required
def quit_from_teacher_group(uid, gid):
    count = TeacherGroupRelation.query.filter(
        TeacherGroupRelation.uid == uid, TeacherGroupRelation.teacher_group_id == gid) \
        .delete()
    msg = str(count) + ' teacher identity has been removed'
    return success_json(msg=msg), 202


@api.route('/<int:oid>/group/lectures', methods=['GET'])
@auth.login_required
def get_teachers_in_org(oid):
    teachers = get_org_teachers_by_group(oid)
    headers = {'Content-Type': 'application/json'}
    t = json.dumps(teachers)
    return t, 200, headers


@api.route('/<int:oid>/lectures', methods=['GET'])
#@auth.login_required
def get_all_teachers_in_org(oid=0):
    if oid==0:
        raise ParamException()
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    total_count, teachers = get_org_teachers(oid, page, per_page)
    headers = {'Content-Type': 'application/json'}
    result = {
        'total_count': total_count,
        'data': teachers
    }
    t = json.dumps(result)
    return t, 200, headers


@api.route('/lecture')
@auth.login_required
def get_lecture():
    args = request.args
    lecture = search_lecture(args)
    headers = {'Content-Type': 'application/json'}
    return lecture, 200, headers


