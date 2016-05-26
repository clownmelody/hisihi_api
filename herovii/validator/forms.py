# -*- coding: utf-8 -*-
from wtforms import TextField
from herovii.settings import PAGE_DEFAULT, PER_PAGE_DEFAULT

__author__ = 'bliss'

from flask import request
from flask_wtf import Form as BaseForm
from wtforms.validators import StopValidation, ValidationError
from werkzeug.datastructures import MultiDict
from .base import *
from herovii.models.user.user import User
from herovii.libs.errors import FormError


class Form(BaseForm):
    @classmethod
    def create_api_form(cls, obj=None, data=None, self_data=None, **args):
        """验证request body或者 args，一次只能验证其中一种类型的参数"""
        # args = request.args
        # json_obj = None
        if not self_data:
            json_obj = request.get_json(silent=True, force=True)
        else:
            # 当self_data!=None 时，不需要Form自动获取request body参数
            json_obj = self_data

        # if json_obj is not None:

        form_data = MultiDict(json_obj)
        # merge = form_data.copy()
        # merge.update(args)
        # else:
        #     # 进入这里，有两种情况一种是args有值，一种是args为[]空值
        #     merge = MultiDict(args)
        form = cls(formdata=form_data, obj=obj, data=data, csrf_enabled=False, **args)
        form._obj = obj
        form.body_data = json_obj
        form.args = obj
        if not form.validate():
            raise FormError(form)
        return form

    def _validate_obj(self, key, value):
        obj = getattr(self, '_obj', None)
        return obj and getattr(obj, key) == value


class UserForm(Form):
    username = StringField(validators=[
        DataRequired(),
        Length(min=3, max=20),
        Regexp(r'^[a-z0-9]+$'),
    ])
    password = PasswordField(validators=[DataRequired()])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise StopValidation('Username has been registered.')


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Email()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise StopValidation('Email has been registered.')


class PhoneNumberForm(Form):
    mobile = StringField(validators=[
        # DataRequired(),
        Length(11),
        Regexp(r'^\d{11}$')
    ])


class SMSCodeForm(Form):
    sms_code = StringField(validators=[
        DataRequired(),
        Length(6),
        Regexp(r'\d{6}$')
    ])


class PasswordForm(Form):
    password = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_]{6,22}$')
    ])


class DownloadPlus1Form(Form):
    oid = create_positive_integer_field()
    channel = StringField(validators=[DataRequired()])


class GetTokenForm(Form):
    account = create_not_empty_field()
    secret = StringField()
    type = StringField(validators=[DataRequired()])
    device = StringField()


class OnlineIDForm(Form):
    oid = create_positive_integer_field()


class RegisterByMobileForm(SMSCodeForm, PhoneNumberForm, PasswordForm):
    pass


class PagingForm(Form):
    page = StringField(default=str(PAGE_DEFAULT))
    per_page = StringField(default=str(PER_PAGE_DEFAULT))

    def validate_page(self, filed):
        if int(filed.data[0]) < 1:
            raise ValidationError('page parameter must be an positive integer')

    def validate_per_page(self, filed):
        if int(filed.data[0]) < 1:
            raise ValidationError('per_page parameter must be an positive integer')


class StatsSignInCountForm(PagingForm):
    since = IntegerField()
    end = IntegerField()


class OrgForm(Form):
    name = StringField(validators=[DataRequired()])
    # uid = IntegerField(validators=[DataRequired()])
    # city = StringField(validators=[DataRequired()])
    #
    type = IntegerField(validators=[DataRequired()])

    phone_num = StringField(validators=[DataRequired()])


class OrgUpdateForm(Form):
    id = IntegerField(validators=[DataRequired()])


class IDForm(Form):
    id = IntegerField(validators=[NumberRange(1)])


class UserCSUChangeIdentityForm(Form):
    uid = IntegerField(validators=[NumberRange(1)])
    group_id = IntegerField(validators=[NumberRange(1)])


class TeacherGroupForm(Form):
    organization_id = IntegerField(validators=[NumberRange(1)])
    title = StringField(validators=[DataRequired()])


class OrgTeacherQuery(Form):
    group = StringField(default='*')


# class OrgLectureQuery(Form):
#     lid = StringField()


class OrgCourseForm(Form):
    organization_id = IntegerField(
        validators=[NumberRange(1), DataRequired()])
    title = StringField(
        validators=[DataRequired()]
    )


class StudentClassForm(Form):
    organization_id = IntegerField(validators=[NumberRange(1), DataRequired()])
    title = StringField(validators=[DataRequired()])
    class_start_date = StringField(validators=[DataRequired(), Regexp(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')])
    class_end_date = StringField(validators=[DataRequired(), Regexp(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')])
    monday = StringField(validators=[Regexp(r'^[1-3]{0,3}$')])
    tuesday = StringField(validators=[Regexp(r'^[1-3]{0,3}$')])
    wednesday = StringField(validators=[Regexp(r'^[1-3]{0,3}$')])
    thursday = StringField(validators=[Regexp(r'^[1-3]{0,3}$')])
    friday = StringField(validators=[Regexp(r'^[1-3]{0,3}$')])
    saturday = StringField(validators=[Regexp(r'^[1-3]{0,3}$')])
    sunday = StringField(validators=[Regexp(r'^[1-3]{0,3}$')])


class StudentClassUpdateForm(Form):
    id = IntegerField(validators=[NumberRange(1), DataRequired()])


class OrgCourseUpdateForm(Form):
    id = IntegerField(
        validators=[NumberRange(1), DataRequired()]
    )


class OrgPicsGetForm(PagingForm):
    type = StringField(default='0')


class OrgPicForm(Form):
    # organization_id = IntegerField(
    #     validators=[NumberRange(1), DataRequired()]
    # )
    url = StringField(
        validators=[DataRequired()]
    )


class OrgPicUpdateForm(Form):
    id = IntegerField(
        validators=[NumberRange(1), DataRequired()]
    )


class VideoUpdateForm(Form):
    id = IntegerField(
        validators=[NumberRange(1), DataRequired()]
    )


class LectureJoinForm(Form):
    uid = IntegerField(validators=[DataRequired(), NumberRange(1)])
    teacher_group_id = IntegerField(validators=[DataRequired(), NumberRange(1)])
    oid = IntegerField(validators=[DataRequired(), NumberRange(1)])
    teacher_good_at_subjects = StringField()
    teacher_introduce = StringField()


class StudentJoinForm(Form):
    uid = IntegerField(validators=[DataRequired(), NumberRange(1)])
    student_class_id = IntegerField(validators=[DataRequired(), NumberRange(1)])


class RegisterForm(UserForm, EmailForm):
    def get_valid_data(self):
        return {
            'username': self.username.data,
            'password': self.password.data,
            'email': self.email.data
        }


class FeedbackForm(Form):
    organization_id = IntegerField(validators=[DataRequired(), NumberRange(1)])
    qq = StringField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])


class YellowPagesForm(Form):
    # id = IntegerField(validators=[DataRequired(), NumberRange(1)])
    web_name = StringField(validators=[DataRequired()])
    url = StringField(validators=[DataRequired()])
    icon_url = StringField(validators=[DataRequired()])
    class_id = IntegerField(validators=[DataRequired(), NumberRange(1)])
    state = IntegerField()
    real_score = IntegerField()
    fake_score = IntegerField()


class UpdateYellowPagesForm(Form):
    # id = IntegerField(validators=[DataRequired(), NumberRange(1)])
    web_name = StringField()
    url = StringField()
    icon_url = StringField()
    class_id = IntegerField(validators=[NumberRange(1)])
    state = IntegerField()
    status = IntegerField()
    fake_score = IntegerField()


class CategoryForm(Form):
    category_name = StringField(validators=[DataRequired()])
    icon_url = StringField(validators=[DataRequired()])


class UpdateCategoryForm(Form):
    # id = IntegerField(validators=[DataRequired(), NumberRange(1)])
    category_name = StringField()
    icon_url = StringField()
    status = IntegerField()


class ClassmateJoinForm(Form):
    uids = StringField(validators=[DataRequired()])
    cid = IntegerField(validators=[DataRequired(), NumberRange(1)])


class FollowUserForm(Form):
    uid = StringField(validators=[DataRequired()])
    recommend_id = StringField(validators=[DataRequired()])
    recommend_type = StringField(validators=[DataRequired()])


class LowPriceFeedbackForm(Form):
    organization_id = IntegerField(validators=[DataRequired(), NumberRange(1)])
    organization_name = StringField(validators=[DataRequired()])
    course_name = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    phone_num = StringField(validators=[DataRequired()])


class OrgTeachingCourseForm(Form):
    organization_id = IntegerField(validators=[NumberRange(1), DataRequired()])
    university_id = IntegerField()
    course_name = StringField(validators=[DataRequired()])
    cover_pic = StringField(validators=[DataRequired()])
    start_course_time = StringField(validators=[DataRequired(), Regexp(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')])
    end_course_time = StringField(validators=[DataRequired(), Regexp(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')])
    lesson_period = IntegerField(validators=[DataRequired(), NumberRange(1)])
    student_num = IntegerField(validators=[DataRequired(), NumberRange(1)])
    lecture_name = StringField(validators=[DataRequired()])
    introduction = StringField(validators=[DataRequired()])
    plan = StringField(validators=[DataRequired()])
    price = IntegerField(validators=[DataRequired(), NumberRange(1)])


class OrgTeachingCourseEnrollForm(Form):
    course_id = IntegerField(validators=[NumberRange(1), DataRequired()])
    uid = IntegerField(validators=[DataRequired()])
    student_name = StringField(validators=[DataRequired()])
    student_phone_num = StringField(validators=[DataRequired()])
    student_university = StringField(validators=[DataRequired()])
    student_qq = StringField()


class UpdateOrgTeachingCourseForm(Form):
    id = IntegerField(validators=[NumberRange(1), DataRequired()])
    organization_id = IntegerField()
    course_name = StringField()
    cover_pic = StringField()
    start_course_time = StringField()
    end_course_time = StringField()
    lesson_period = IntegerField()
    student_num = IntegerField()
    lecture_name = StringField()
    price = IntegerField()
    introduction = StringField(validators=[DataRequired()])
    plan = StringField(validators=[DataRequired()])


class NewsForm(Form):
    organization_id = IntegerField(validators=[NumberRange(1), DataRequired()])
    tag = StringField(validators=[DataRequired()])
    title = StringField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])


class UpdateNewsForm(Form):
    id = IntegerField(validators=[NumberRange(1), DataRequired()])
    tag = StringField()
    title = StringField()
    content = StringField()


class OrgUniversityEnrollForm(Form):
    university_id = IntegerField(validators=[NumberRange(1), DataRequired()])
    uid = IntegerField(validators=[DataRequired()])
    student_name = StringField(validators=[DataRequired()])
    student_phone_num = StringField(validators=[DataRequired()])
    student_education = StringField(validators=[DataRequired()])
    student_qq = StringField()
    study_abroad_purpose = StringField(validators=[DataRequired()])
    apply_major = StringField(validators=[DataRequired()])


class OverseaPlanUpdateForm(Form):
    id = IntegerField(validators=[DataRequired()])
    html_content = StringField()
    url = StringField(validators=[DataRequired()])


class OverseaPlanAddForm(Form):
    oid = IntegerField(validators=[DataRequired()])
    html_content = StringField()
    url = StringField(validators=[DataRequired()])


class OverseaPlanForm(Form):
    id = IntegerField(validators=[DataRequired()])
    url = StringField(validators=[DataRequired()])


class ObtainCouponForm(Form):
    uid = IntegerField(validators=[DataRequired()])
    coupon_id = IntegerField(validators=[DataRequired()])


class ObtainGiftPackageForm(Form):
    uid = IntegerField(validators=[DataRequired()])
    obtain_coupon_record_id = IntegerField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    phone_num = StringField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired()])
