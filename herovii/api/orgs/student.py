import datetime
from flask import jsonify
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import IllegalOperation
from herovii.libs.util import is_today
from herovii.models.base import db
from herovii.models.org.sign_in import StudentSignIn
from herovii.models.org.student_class import StudentClass
from herovii.models.org.student_class_relation import StudentClassRelation
from herovii.models.org.student_class_stats import StudentClassStats
from herovii.validator.forms import StudentClassForm, StudentJoinForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/<int:oid>/student/<int:uid>/sign-in/<date>', methods=['POST'])
@auth.login_required
def student_sign_in(oid, uid, date):
    date_sign_in = datetime.datetime.strptime(date, '%Y-%m-%d')
    today = is_today(date_sign_in)

    if not today:
        raise IllegalOperation(error='date is not today')

    sign_in = StudentSignIn.query.filter(
        StudentSignIn.date == date, StudentSignIn.uid == uid,
        StudentSignIn.organization_id == oid).first()

    if sign_in:
        return jsonify(sign_in), 201

    with db.auto_commit():
        sign_in = StudentSignIn()
        sign_in.organization_id = oid
        sign_in.date = date
        sign_in.uid = uid
        db.session.add(sign_in)
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

    stats_class = StudentClassStats()
    with db.auto_commit():
        db.session.add(s_class)
        stats_class.student_class_id = stats_class.id
        db.session.add(stats_class)
    return jsonify(s_class), 201


@api.route('/student/class/join', method=['POST'])
def move_student_to_class():
    form = StudentJoinForm.create_api_form()
    s_c_relation = StudentClassRelation()
    s_c_relation.uid = form.uid.data
    s_c_relation.student_class_id = form.student_class_id.data

    with db.auto_commit():
        db.session.add(s_c_relation)
        StudentClassStats.query.filter_by(student_class_id=form.student_class_id.data).\
            update({StudentClassStats.value: StudentClassStats.value+1})
    return jsonify(s_c_relation), 201



