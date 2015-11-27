from flask.ext.wtf.file import FileField
from wtforms.fields.core import BooleanField

__author__ = 'bliss'

from flask import request
from flask_wtf import Form as BaseForm
from wtforms.validators import StopValidation, ValidationError
from werkzeug.datastructures import MultiDict
from .base import *
from herovii.models.user.user import User
from herovii.libs.errors import FormError
from herovii.libs.error_code import JSONStyleError


class Form(BaseForm):
    @classmethod
    def create_api_form(cls, obj=None, data=None, **args):
        # args = request.args
        json_obj = request.get_json(silent=True, force=True)
        # if not json_obj and not args and not ignore_none:
        #     # 当POST body 和 args参数都为None，且不允许忽略空值时，抛出异常
        #     # 注意，空参数且需要验证的情况，仅出现在form有给参数赋予默认值的情况下
        #     # 比如 分页参数，page和count，他们都可以不传递，form会自动为其赋值
        #     raise JSONStyleError()

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
        DataRequired(),
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
    page = StringField(default='1')
    per_page = StringField(default='20')

    def validate_page(self, filed):
        if int(filed.data[0]) < 1:
            raise ValidationError('Name must be less than 50 characters')

    def validate_per_page(self, filed):
        if int(filed.data[0]) < 1:
            raise ValidationError('Name must be less than 50 characters')


class OrgForm(Form):
    name = StringField(validators=[DataRequired()])


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


class OrgCourseForm(Form):
    organization_id = IntegerField(
        validators=[NumberRange(1), DataRequired()])
    title = StringField(
        validators=[DataRequired()]
    )


class OrgCourseUpdateForm(OrgCourseForm):
    id = IntegerField(
        validators=[NumberRange(1), DataRequired()]
    )


class RegisterForm(UserForm, EmailForm):

    def get_valid_data(self):
        return {
            'username': self.username.data,
            'password': self.password.data,
            'email': self.email.data
        }

