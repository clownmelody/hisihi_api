from flask import jsonify, json
from flask.globals import request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import NotFound, ParamException
from herovii.libs.util import validate_int_arguments, validate_date_arguments
from herovii.service.org import view_student_count, view_sign_in_count, view_sign_in_count_single, \
    get_org_list_class_sign_in_count_stats
from herovii.validator.forms import StatsSignInCountForm, PagingForm

__author__ = 'bliss'


api = ApiBlueprint('org')


@api.route('/<int:oid>/student/enroll/stats/count')
@auth.login_required
def get_student_stats_count(oid):
    counts = view_student_count(oid)
    if not counts:
        raise NotFound(error='no student in organization')
    data = {
        'in_count': counts[1],
        'standby_count': counts[0]
    }
    headers = {'Content-Type': 'application/json'}
    return jsonify(data), 200, headers


@api.route('/<int:oid>/student/sign-in/stats/count')
@auth.login_required
def get_sign_in_count_stats(oid):
    args = request.args.to_dict()
    form = StatsSignInCountForm.create_api_form(**args)
    dto = view_sign_in_count(oid, form)
    headers = {'Content-Type': 'application/json'}
    return json.dumps(dto), 200, headers


@api.route('/<int:oid>/student/sign-in/<date>/stats/count')
@auth.login_required
def get_sign_in_count_status_single(oid, date):
    sign_in = view_sign_in_count_single(oid, date)
    return jsonify(sign_in), 200


@api.route('/<int:oid>/class/sign-in/<date>/stats/count')
def get_list_class_sign_in_count_stats(oid, date):
    """获取签到情况，按班级分类
       oid : 机构id号
       date: 日期 2015-12-10
    """
    # Todo: @楚杰
    if not validate_int_arguments(oid):
        raise ParamException(error='organization id arguments is empty',
                             error_code=1001, code=200)
    date = validate_date_arguments(date)
    if not date:
        raise ParamException(error='date arguments exception',
                             error_code=1001, code=200)
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = (1 if form.page.data else form.page.data)
    per_page = (20 if form.per_page.data else form.per_page.data)
    total_count, data = get_org_list_class_sign_in_count_stats(oid, date, page, per_page)
    headers = {'Content-Type': 'application/json'}
    result = {
        'total_count': total_count,
        'data': data
    }
    return json.dumps(result), 200, headers

