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


@api.route('/enroll/blz/<int:blz_id>')
def view_blz(blz_id):
    """查看订单详情
       blz_id: 订单号
       请完成接口并测试后在方法上添加@auth.login_required
       最后在docs/classmate 里编写文档
    """
    # Todo: @杨楚杰
    pass


@api.route('/enroll/blz', methods=['PUT'])
def update_blz():
    """查看订单详情
       输入：PUT 一个 Enroll 对象（支持部分属性更新）
       请完成接口并测试后在方法上添加@auth.login_required
       最后在docs/classmate 里编写文档
    """
    # Todo: @杨楚杰
    pass


