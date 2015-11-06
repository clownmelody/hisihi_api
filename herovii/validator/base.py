__author__ = 'bliss'

from wtforms.fields import StringField, PasswordField, IntegerField
from wtforms.validators import Email, Length, Regexp, NumberRange, DataRequired


def create_positive_integer_field():
    return IntegerField(validators=[
        DataRequired(),
        NumberRange(1)
    ])


def create_not_empty_field():
    return StringField(validators=[
        DataRequired(),
        Length(min=1)
    ])

