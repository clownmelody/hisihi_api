from flask import jsonify
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.validator.forms import OrgForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('', methods=['POST'])
@auth.login_required
def create_org():
    org = OrgForm.create_api_form()
    create_org(org)
    return jsonify(org), 201


@auth.login_required
@api.route('', methods=['PUT'])
def update_org():
    return 'ok put'


