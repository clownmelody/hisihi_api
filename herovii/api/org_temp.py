# import datetime
# from flask import jsonify, g, json, request
# from herovii.libs.bpbase import ApiBlueprint, auth
# from herovii.libs.error_code import IllegalOperation, OrgNotFound, UnknownError, ParamException, \
#     VolumeTooLarge, NotFound
# from herovii.libs.httper import BMOB
# from herovii.libs.helper import success_json
# from herovii.libs.util import is_today
# from herovii.models.base import db
# from herovii.models.org.course import Course
# from herovii.models.org.info import Info
# from herovii.models.org.pic import Pic
# from herovii.models.org.qrcode import QrcodeSignIn
# from herovii.models.org.sign_in import StudentSignIn
# from herovii.service import account
# from herovii.service.org import create_org_info, dto_org_courses_paginate, \
#     get_course_by_id, create_org_pics, view_student_count
# from herovii.service.news import get_news_dto_paginate
# from herovii.validator.forms import OrgForm, OrgUpdateForm, RegisterByMobileForm, PagingForm, \
#     OrgCourseForm, OrgCourseUpdateForm, OrgPicForm
# from herovii.service.user_org import register_by_mobile
#
# __author__ = 'bliss'
#
# api = ApiBlueprint('org')
#
#
# # @api.route('/<int:oid>/pics', methods=['POST'])
# # @auth.login_required
# # def upload_pic(oid):
# #     org_info = Info.query.filter_by(uid=g.user[0]).first()
# #
# #     if org_info.id != oid:
# #         raise IllegalOperation()
# #     temp_pics = request.get_json(silent=True, force=True)
# #     if not temp_pics:
# #         raise ParamException()
# #     if len(temp_pics) >= 20:
# #         raise VolumeTooLarge()
# #
# #     pics = []
# #     for temp_pic in temp_pics:
# #         OrgPicForm.create_api_form(self_data=temp_pic)
# #         temp_pic['organization_id'] = oid
# #         pic = Pic()
# #         for key, value in temp_pic.items():
# #             setattr(pic, key, value)
# #         pics.append(pic)
# #     r_pics = create_org_pics(pics)
# #     str_data = json.dumps(r_pics)
# #     headers = {'Content-Type': 'application/json'}
# #     return str_data, 201, headers
#
#
# <<<<<<< HEAD
# =======
# @api.route('/admin/password', methods=['PUT'])
# def find_admin_password():
#     """ 重置/找回密码
#         调用此接口需要先调用'/v1/sms/verify' 接口，以获得短信验证码
#     :PUT:
#         {"phone_number":'18699998888', "sms_code":'876876', "password":'password'}
#     :return:
#     """
#     bmob = BMOB()
#     form = RegisterByMobileForm.create_api_form()
#     mobile = form.phone_number.data
#     password = form.password.data
#     sms_code = form.sms_code.data
#     status, body = bmob.verify_sms_code(mobile, sms_code)
#     if status == 200:
#         account.reset_password_by_mobile(mobile, password)
#         return success_json(), 202
#     else:
#         j = json.loads(body)
#         raise UnknownError(j['error'], error_code=None)
#
#
# @api.route('/news', methods=['GET'])
# @auth.login_required
# def list_news():
#     args = request.args.to_dict()
#     form = PagingForm.create_api_form(**args)
#     news = get_news_dto_paginate(int(form.page.data), int(form.per_page.data))
#     headers = {'Content-Type': 'application/json'}
#     return json.dumps(news), 200, headers
#
#
# @api.route('/admin/<int:id>', methods=['GET'])
# def get_org_admin(id):
#     pass
#
#
# @api.route('/admin/<int:id>', methods=['PUT'])
# def update_org_admin(id):
#     pass
#
#
# @api.route('/course', methods=['POST'])
# @auth.login_required
# def create_org_course():
#     form = OrgCourseForm.create_api_form()
#     course = Course()
#     for key, value in form.body_data.items():
#         setattr(course, key, value)
#     with db.auto_commit():
#         db.session.add(course)
#     return jsonify(course), 201
#
#
# @api.route('/course', methods=['PUT'])
# @auth.login_required
# def update_org_course():
#     form = OrgCourseUpdateForm.create_api_form()
#     course = Course.query.filter_by(id=form.id.data).first_or_404()
#     with db.auto_commit():
#         for key, value in form.body_data.items():
#             setattr(course, key, value)
#     return jsonify(course), 202
#
#
# @api.route('/course/<int:cid>', methods=['DELETE'])
# @auth.login_required
# def delete_org_course(cid):
#     Course.query.filter_by(id=cid).delete()
#     return success_json(), 202
#
#
# @api.route('/<int:oid>/courses')
# @auth.login_required
# def list_courses(oid):
#     args = request.args
#     form = PagingForm.create_api_form(**args)
#     dto = dto_org_courses_paginate(oid, form.page.data[0], form.per_page.data[0])
#     headers = {'Content-Type': 'application/json'}
#     json_obj = json.dumps(dto)
#     return json_obj, 200, headers
#
#
# @api.route('/courses/<int:cid>')
# @auth.login_required
# def get_course(cid):
#     course = get_course_by_id(cid)
#     json_data = json.dumps(course)
#     headers = {'Content-Type': 'application/json'}
#     return json_data, 200, headers
#
#
# @api.route('/<int:oid>/pics', methods=['POST'])
# @auth.login_required
# def upload_pic(oid):
#     org_info = Info.query.filter_by(uid=g.user[0]).first()
#
#     if org_info.id != oid:
#         raise IllegalOperation()
#     temp_pics = request.get_json(silent=True, force=True)
#     if not temp_pics:
#         raise ParamException()
#     if len(temp_pics) >= 20:
#         raise VolumeTooLarge()
#
#     pics = []
#     for temp_pic in temp_pics:
#         OrgPicForm.create_api_form(self_data=temp_pic)
#         temp_pic['organization_id'] = oid
#         pic = Pic()
#         for key, value in temp_pic.items():
#             setattr(pic, key, value)
#         pics.append(pic)
#     r_pics = create_org_pics(pics)
#     str_data = json.dumps(r_pics)
#     headers = {'Content-Type': 'application/json'}
#     return str_data, 201, headers
#
#
# @api.route('/<int:oid>/student/stats/count')
# @auth.login_required
# def get_student_stats_count(oid):
#     counts = view_student_count(oid)
#     if not counts:
#         raise NotFound(error='no student in organization')
#     data = {
#         'student_in_count': counts[1],
#         'student_standby_count': counts[0]
#     }
#     return jsonify(data), 200
#
#
# @api.route('/<int:oid>/qrcode/sign-in/today', methods=['POST'])
# @auth.login_required
# def get_qrcode_sign_in_today(oid):
#     today = datetime.datetime.now()
#     date_str = today.strftime('%Y-%m-%d')
#     qrcode = QrcodeSignIn.query.filter_by(
#         organization_id=oid, date=date_str).first()
#     if qrcode:
#         return jsonify(qrcode), 201
#     qrcode = QrcodeSignIn(oid, today)
#     qrcode.make()
#     with db.auto_commit():
#         db.session.add(qrcode)
#     return jsonify(qrcode), 201
#
#
# @api.route('/<int:oid>/student/<int:uid>/sign-in/<date>', methods=['POST'])
# @auth.login_required
# def student_sign_in(oid, uid, date):
#     date_sign_in = datetime.datetime.strptime(date, '%Y-%m-%d')
#     today = is_today(date_sign_in)
#
#     if not today:
#         raise IllegalOperation(error='date is not today')
#
#     sign_in = StudentSignIn.query.filter(
#         StudentSignIn.date == date, StudentSignIn.uid == uid,
#         StudentSignIn.organization_id == oid).first()
#
#     if sign_in:
#         return jsonify(sign_in), 201
#
#     with db.auto_commit():
#         sign_in = StudentSignIn()
#         sign_in.organization_id = oid
#         sign_in.date = date
#         sign_in.uid = uid
#         db.session.add(sign_in)
#     return jsonify(sign_in), 201
#
# >>>>>>> d7fc69abbf71e44b1ca3a7450856bd6bae0d8dd5
#
#
#
#
#
