import datetime
from flask import jsonify
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import IllegalOperation
from herovii.libs.util import is_today
from herovii.models.base import db
from herovii.models.org.sign_in import StudentSignIn

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