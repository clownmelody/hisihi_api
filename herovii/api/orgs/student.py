import datetime
from flask import jsonify
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import IllegalOperation
from herovii.libs.util import is_today
from herovii.models.base import db
from herovii.models.org.student_class import StudentClass
from herovii.models.org.classmate import Classmate
from herovii.service.org import create_student_sign_in
from herovii.validator.forms import StudentClassForm, StudentJoinForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/<int:oid>/student/<int:uid>/sign-in/<date>', methods=['POST'])
@auth.login_required
def student_sign_in(oid, uid, date):
    # init_classmate_mirror(oid, date)
    date_sign_in = datetime.datetime.strptime(date, '%Y-%m-%d')
    today = is_today(date_sign_in)

    if not today:
        raise IllegalOperation(error='date is not today')

    today_str = date_sign_in.strftime('%Y-%m-%d')
    sign_in = create_student_sign_in(oid, uid, today_str)
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


@api.route('/student/<int:uid>/profile')
def get_student_profile(uid):
    """获取学生资料
       uid: 学生id号
       请完成接口并测试后在方法上添加@auth.login_required
       最后在docs/student 里编写文档
    """
    # Todo: @杨楚杰
    pass


@api.route('/student/<int:uid>/sign-in/history')
def get_student_sign_in_history(uid):
    """获取学生历史签到记录
       uid: 学生id号
       请完成接口并测试后在方法上添加@auth.login_required
       最后在docs/student 里编写文档
    """
    # Todo: @杨楚杰
    pass





