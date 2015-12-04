from flask import jsonify
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import NotFound
from herovii.service.org import view_student_count
from herovii.validator.forms import PagingForm

__author__ = 'bliss'


api = ApiBlueprint('org')


@api.route('/<int:oid>/enroll/stats/count')
@auth.login_required
def get_student_stats_count(oid):
    form = PagingForm.create_api_form()
    counts = view_student_count(oid)
    if not counts:
        raise NotFound(error='no student in organization')
    data = {
        'in_count': counts[1],
        'standby_count': counts[0]
    }
    return jsonify(data), 200


@api.route('/<int:oid>/sign-in/status/count')
def get_sign_in_count_stats(oid):
    pass


@api.route('/<int:oid>/team/sign-in/status/count')
def get_list_class_sign_in_count_status(oid):
    pass
