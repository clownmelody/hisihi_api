import json
from flask.globals import request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import ParamException
from herovii.libs.util import validate_int_arguments, validate_date_arguments
from herovii.service.org import get_class_sign_in_detail_by_date, get_org_class_all_students_service
from herovii.validator.forms import PagingForm

__author__ = 'bliss'


api = ApiBlueprint('org')


@api.route('/<int:oid>/class/<int:cid>/sign-in/<date>/detail', methods=['GET'])
def get_org_class_sign_in_detail_by_data(oid, cid, date):
    """获取签到情况，按班级分类
       oid : 机构id号
       date: 日期 2015-12-10
       cid: 班级号
    """
    # Todo: @杨楚杰
    if not validate_int_arguments(oid):
        raise ParamException(error='organization id arguments is empty')
    if not validate_int_arguments(cid):
        raise ParamException(error='class id arguments is empty')
    date = validate_date_arguments(date)
    if not date:
        raise ParamException(error='date arguments exception')
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    data, total_count, sign_in_count, unsign_in_count = get_class_sign_in_detail_by_date(oid, cid, date, page, per_page)
    result = {
        "data": data,
        "total_count": total_count,
        "sign_in_count": sign_in_count,
        "unsign_in_count": unsign_in_count
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers


@api.route('/<int:oid>/class/<int:cid>/students', methods=['GET'])
# @auth.login_required
# 获取班级下所有学生列表
def get_org_class_all_students(oid, cid):
    if not validate_int_arguments(oid):
        raise ParamException(error='organization id arguments is empty')
    if not validate_int_arguments(cid):
        raise ParamException(error='class id arguments is empty')
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    data, total_count = get_org_class_all_students_service(oid, cid, page, per_page)
    result = {
        "data": data,
        "total_count": total_count
    }
    headers = {'Content-Type': 'application/json'}
    return json.dumps(result), 200, headers
