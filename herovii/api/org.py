from flask import jsonify, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.models.org import Org
from herovii.service.org import create_org_info
from herovii.validator.forms import OrgForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('', methods=['POST'])
@auth.login_required
def create_org():
    form = OrgForm.create_api_form()
    post_data = form.body_data
    org = Org(**post_data)
    create_org_info(org)
    return jsonify(org), 201


@auth.login_required
@api.route('', methods=['PUT'])
def update_org():
    return 'ok put'


