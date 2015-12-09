from flask import json
from flask.globals import request
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import NotFound
from herovii.service.org import dto_get_blzs_paginate
from herovii.validator.forms import PagingForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/<int:oid>/enroll/blzs')
def list_blzs(oid):
    # TODO: remember return user's tel and aver
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    blzs = dto_get_blzs_paginate(int(form.page.data), int(form.per_page.data), oid)
    if not blzs:
        raise NotFound()
    blzs_json = json.dumps(blzs)
    headers = {'Content-Type': 'application/json'}
    return blzs_json, 200, headers


@api.route('/<int:oid>/enroll/blzs/<int:blz_id>')
def view_blz(oid, blz_id):
    pass

