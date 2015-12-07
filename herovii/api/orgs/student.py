import datetime
from flask import jsonify
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import IllegalOperation
from herovii.libs.util import is_today
from herovii.models.base import db
from herovii.models.org.student_class import StudentClass
from herovii.models.org.classmate import Classmate
# from herovii.models.org.student_class_stats import StudentClassStats
from herovii.service.org import create_student_sign_in, init_classmate_mirror
from herovii.validator.forms import StudentClassForm, StudentJoinForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/<int:oid>/student/<int:uid>/sign-in/<date>', methods=['POST'])
# @auth.login_required
def student_sign_in(oid, uid, date):
    init_classmate_mirror(oid, date)
    date_sign_in = datetime.datetime.strptime(date, '%Y-%m-%d')
    today = is_today(date_sign_in)

    if not today:
        raise IllegalOperation(error='date is not today')

    sign_in = create_student_sign_in(oid, uid, date)
    return jsonify(sign_in), 201


@api.route('/<int:oid>/class/<int:cid>/sign-in')
def get_class_sign_in_detail(oid, cid):
    pass


@api.route('/student/class', methods=['POST'])
def create_student_class():
    form = StudentClassForm.create_api_form()
    s_class = StudentClass()
    s_class.organization_id = form.organization_id.data
    s_class.title = form.title.data

    # stats_class = StudentClassStats()
    with db.auto_commit():
        db.session.add(s_class)
    return jsonify(s_class), 201


@api.route('/student/class/join', methods=['POST'])
def move_student_to_class():
    form = StudentJoinForm.create_api_form()
    s_c_relation = Classmate()
    s_c_relation.uid = form.uid.data
    s_c_relation.student_class_id = form.student_class_id.data

    with db.auto_commit():
        db.session.add(s_c_relation)
    return jsonify(s_c_relation), 201



