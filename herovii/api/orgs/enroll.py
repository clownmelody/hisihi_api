from flask import json, jsonify
from flask.globals import request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import NotFound, ParamException, UpdateDBError
from herovii.libs.util import validate_int_arguments
from herovii.service.enroll import get_stu_enroll_detail_info, update_stu_enroll_info
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


@api.route('/enroll/blz/<int:blz_id>', methods=['GET'])
@auth.login_required
def view_blz(blz_id):
    """查看订单详情
       blz_id: 订单号
    """
    # Todo: @杨楚杰
    if not validate_int_arguments(blz_id):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    student = get_stu_enroll_detail_info(blz_id)
    headers = {'Content-Type': 'application/json'}
    student_json = jsonify(student)
    return student_json, 200, headers


@api.route('/enroll/blz/<int:blz_id>', methods=['PUT'])
@auth.login_required
def update_blz(blz_id):
    """查看订单详情
       输入：PUT 一个 Enroll 对象（支持部分属性更新）
    """
    # Todo: @杨楚杰
    req = request.get_json(silent=True, force=True)
    if not validate_int_arguments(blz_id):
        raise ParamException(error='arguments is empty',
                             error_code=1001, code=200)
    if not req['status']:
        raise ParamException(error='the data to update is empty',
                             error_code=1001, code=200)
    status = req['status']
    if status != 2 and status != -2:
        raise ParamException(error='the status is limited to be 2 or -2',
                             error_code=1001, code=200)
    data = {
        "blz_id": blz_id,
        "status": status
    }
    res = update_stu_enroll_info(data)
    if res:
        headers = {'Content-Type': 'application/json'}
        return jsonify(res), 202, headers
    else:
        raise UpdateDBError()




