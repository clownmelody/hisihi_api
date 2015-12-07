
from flask import jsonify, json
from herovii.libs.bpbase import ApiBlueprint, auth

from herovii.libs.helper import success_json
from herovii.models.base import db

from herovii.models.org.teacher_group import TeacherGroup
from herovii.models.org.teacher_group_relation import TeacherGroupRelation
from herovii.models.user.user_csu import UserCSU

from herovii.service.org import  get_org_teachers_by_group
from herovii.validator.forms import TeacherGroupForm, LectureJoinForm

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
    t_g_realation = TeacherGroupRelation()
    t_g_realation.teacher_group_id = form.teacher_group_id.data
    t_g_realation.uid = form.uid.data
    with db.auto_commit():
        db.session.add(t_g_realation)
    return jsonify(t_g_realation), 201


@api.route('/lecture/<int:uid>/group/<int:gid>/quite', methods=['DELETE'])
@auth.login_required
def quit_from_teacher_group(uid, gid):
    count = TeacherGroupRelation.query.filter(
        TeacherGroupRelation.uid == uid, TeacherGroupRelation.teacher_group_id == gid) \
        .delete()
    msg = count + 'teacher identity has been removed'
    return success_json(msg=msg), 202


@api.route('/<int:oid>/group/lectures', methods=['GET'])
@auth.login_required
def get_teachers_in_org(oid):
    teachers = get_org_teachers_by_group(oid)
    headers = {'Content-Type': 'application/json'}
    t = json.dumps(teachers)
    return t, 200, headers


@api.route('/lecture/<int:lid>')
def get_lecture(lid):
    lecture = UserCSU.query.get(lid)
    return jsonify(lecture), 200

