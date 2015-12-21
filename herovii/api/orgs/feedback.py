from flask import jsonify, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.models.org.feedback import Feedback
from herovii.models.base import db
from herovii.validator.forms import FeedbackForm

__author__ = 'shaolei'

api = ApiBlueprint('org')


@api.route('/feedback/post', methods=['POST'])
def create_feedback():
    form = FeedbackForm.create_api_form()
    with db.auto_commit():
        feedback = Feedback()
        feedback.organization_id = form.organization_id.data
        feedback.admin_id = form.admin_id.data
        feedback.qq = form.qq.data
        feedback.content = form.content.data
        db.session.add(feedback)
    return jsonify(feedback), 201





