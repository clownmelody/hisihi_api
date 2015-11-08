__author__ = 'bliss'

from flask import request
from flask_wtf import Form as BaseForm
from wtforms.validators import StopValidation
from werkzeug.datastructures import MultiDict
from .base import *
from herovii.models import User
from herovii.libs.errors import FormError
from herovii.libs.error_code import ParamException
from wtforms import Field


class Form(BaseForm):
    @classmethod
    def create_api_form(cls, obj=None):
        args = request.args
        # r_data = request.get_data()
        # lt = eval(r_data)
        # form_data = MultiDict(lt)
        data = request.get_json(silent=True, force=True)
        if not data:
            raise ParamException(error=('the input json data is invalid,caution: '
                                        'the name of json data,should be'
                                        'in double quotation marks'))

        form_data = MultiDict(request.get_json(silent=True, force=True))

        merge = form_data.copy()
        merge.update(args)
        form = cls(formdata=merge, obj=obj, csrf_enabled=False)
        form._obj = obj
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
    phone_number = StringField(validators=[
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
        # password can only include lettes , numbers and "_"
        Regexp(r'^[A-Za-z0-9_]{6,22}$')
    ])


class DownloadPlus1Form(Form):
    oid = create_positive_integer_field()
    channel = StringField(validators=[DataRequired()])


class GetTokenForm(Form):
    uid = create_not_empty_field()
    secret = create_not_empty_field()
    type = StringField(validators=[DataRequired()])


class OnlineIDForm(Form):
    oid = create_positive_integer_field()


class RegisterByMobileForm(SMSCodeForm, PhoneNumberForm, PasswordForm):
    pass


class RegisterForm(UserForm, EmailForm):

    def get_valid_data(self):
        return {
            'username': self.username.data,
            'password': self.password.data,
            'email': self.email.data
        }

