import datetime
from flask import jsonify, g, json, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import IllegalOperation, OrgNotFound, UnknownError, ParamException, \
    VolumeTooLarge, NotFound
from herovii.libs.httper import BMOB
from herovii.libs.helper import success_json
from herovii.libs.util import is_today
from herovii.models.base import db
from herovii.models.org.course import Course
from herovii.models.org.info import Info
from herovii.models.org.pic import Pic
from herovii.models.org.qrcode import QrcodeSignIn
from herovii.models.org.sign_in import StudentSignIn
from herovii.service import account
from herovii.service.org import create_org_info, dto_org_courses_paginate, \
    get_course_by_id, create_org_pics, view_student_count
from herovii.service.news import get_news_dto_paginate
from herovii.validator.forms import OrgForm, OrgUpdateForm, RegisterByMobileForm, PagingForm, \
    OrgCourseForm, OrgCourseUpdateForm, OrgPicForm
from herovii.service.user_org import register_by_mobile

__author__ = 'bliss'

api = ApiBlueprint('org')


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







