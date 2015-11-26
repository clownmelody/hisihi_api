from flask import jsonify, g
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import IllegalOperation, OrgNotFound
from herovii.models.base import db
from herovii.models.org.org_info import OrgInfo
from herovii.models.org.teacher_group import TeacherGroup
from herovii.models.org.teacher_group_realation import TeacherGroupRealation
from herovii.service.org import create_org_info, get_org_teachers_by_group
from herovii.validator.forms import OrgForm, OrgUpdateForm, TeacherGroupForm

__author__ = 'bliss'

api = ApiBlueprint('org')


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


@api.route('/group/teacher', methods=['POST'])
def create_teacher_group():
    form = TeacherGroupForm.create_api_form()
    group = TeacherGroup()
    with db.auto_commit():
        group.organization_id = form.organization_id.data
        group.title = form.title.data
    return jsonify(group), 201


@api.route('/group/<int:g_id>/teacher/<int:uid>/join', methods=['POST'])
def join_teacher_group(uid, g_id):
    t_g_realation = TeacherGroupRealation()
    t_g_realation.teacher_group_id = g_id
    t_g_realation.uid = uid
    with db.auto_commit():
        db.session.add(t_g_realation)
    return jsonify(t_g_realation)


@api.route('/<int:oid>/teachers', methods=['GET'])
def get_teachers_in_org(oid):
    get_org_teachers_by_group(oid)


@api.route('/<int:oid>', methods=['GET'])
@auth.login_required
def get_org(oid):
    org_info = OrgInfo.query.get(oid)
    if not org_info:
        raise OrgNotFound()
    if org_info.uid != g.user[0]:
        raise IllegalOperation()
    return jsonify(org_info), 200

