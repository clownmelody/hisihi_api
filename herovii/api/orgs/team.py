from flask import jsonify
from herovii.libs.bpbase import ApiBlueprint
from herovii.models.base import db
from herovii.models.org.student_class import StudentClass
from herovii.validator.forms import StudentClassForm

__author__ = 'bliss'


api = ApiBlueprint('org')


