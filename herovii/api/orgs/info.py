from flask import jsonify
from flask.globals import g, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import NotFound, IllegalOperation, JSONStyleError
from herovii.libs.helper import is_first_party_cms, success_json
from herovii.models.base import db
from herovii.models.org.info import Info
from herovii.service.org import create_org_info, get_org_by_id, get_org_by_uid, update_teachers_field_info, \
    add_major_to_org
from herovii.validator.forms import OrgForm, OrgUpdateForm

__author__ = 'bliss'


api = ApiBlueprint('org')


@api.route('', methods=['POST'])
@auth.login_required
def create_org():
    form = OrgForm.create_api_form()
    post_data = form.body_data

    uid = g.user[0]
    if not uid:
        raise IllegalOperation(error="token identity is invalid to create org")
    post_data['uid'] = uid
    org = Info(**post_data)
    org = create_org_info(org)
    return jsonify(org), 201


@api.route('', methods=['PUT'])
@auth.login_required
def update_org():
    form = OrgUpdateForm().create_api_form()
    org_id = form.id.data
    org_info = Info.query.get(org_id)
    if not org_info:
        raise NotFound(error='organization not found')
    if org_info.uid != g.user[0]:
        raise IllegalOperation()

    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(org_info, key, value)
            if key == 'name':
                update_teachers_field_info(org_id, value)
    return jsonify(org_info), 202


@api.route('', methods=['GET'])
@auth.login_required
def get_org():
    uid = request.args.get('uid')
    oid = request.args.get('oid')

    if oid:
        org_info = get_org_by_id(oid)
        return jsonify(org_info)
    if uid:
        if is_first_party_cms():
            org_info = get_org_by_uid(uid)
            return jsonify(org_info), 200
        else:
            raise IllegalOperation()

    uid = g.user[0]
    org_info = get_org_by_uid(uid)
    if not org_info:
        raise NotFound('organization not found', error_code=5000)
    if org_info.uid != g.user[0]:
        raise IllegalOperation()
    return jsonify(org_info), 200


@api.route('/major', methods=['POST'])
@auth.login_required
def add_org_major():
    json_data = request.get_json(force=True, silent=True)
    if not json_data:
        try:
            oid = request.values.get('oid')
            tag_id = request.values.get('major_id')
        except:
            raise JSONStyleError()
    else:
        oid = json_data['oid']
        tag_id = json_data['major_id']
    msg = add_major_to_org(oid, tag_id)
    headers = {'Content-Type': 'application/json'}
    return success_json(msg=msg), 201, headers

