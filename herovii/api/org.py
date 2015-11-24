from flask import jsonify, g
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import NotFound, IllegalOperation, OrgNotFound
from herovii.models.base import db
from herovii.models.org import OrgInfo
from herovii.service.org import create_org_info
from herovii.validator.forms import OrgForm, OrgUpdateForm

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
        print(org_info.uid)
        print(g.user[0])
        raise IllegalOperation()

    # form.populate_obj(org_info)
    with db.auto_commit():
        # org_info.__dict__.update(**form.body_data)
        for key, value in form.body_data.items():
            setattr(org_info, key, value)
    return jsonify(org_info), 202


@api.route('/<int:oid>', methods=['GET'])
# @auth.login_required
def get_org(oid):
    org_info = OrgInfo.query.get(oid)
    if not org_info:
        raise OrgNotFound()
    # if org_info.uid != g.user[0]:
    #     raise IllegalOperation()
    return jsonify(org_info), 200

