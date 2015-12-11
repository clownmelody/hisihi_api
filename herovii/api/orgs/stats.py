from flask import jsonify, json
from flask.globals import request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import NotFound
from herovii.service.org import view_student_count, view_sign_in_count, view_sign_in_count_single
from herovii.validator.forms import StatsSignInCountForm

__author__ = 'bliss'


api = ApiBlueprint('org')


@api.route('/<int:oid>/student/enroll/stats/count')
@auth.login_required
def get_student_stats_count(oid):
    counts = view_student_count(oid)
    if not counts:
        raise NotFound(error='no student in organization')
    data = {
        'in_count': counts[1][0],
        'standby_count': counts[0][0]
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
       分页参数：page， per_page (可选)， 参见get_sin_in_count_stats 处理方式
       oid : 机构id号
       date: 日期 2015-12-10
       请完成接口并测试后在方法上添加@auth.login_required
       最后在docs/stats 里编写文档
    """
    # Todo: @楚杰
    pass

