import json
from flask import jsonify, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.models.org.feedback import Feedback
from herovii.models.base import db
from herovii.models.org.lowprice_feedback import LowPriceFeedback
from herovii.validator.forms import FeedbackForm, LowPriceFeedbackForm

__author__ = 'shaolei'

api = ApiBlueprint('org')


@api.route('/feedback/advice', methods=['POST'])
@auth.login_required
def create_feedback():
    form = FeedbackForm.create_api_form()
    with db.auto_commit():
        feedback = Feedback()
        feedback.organization_id = form.organization_id.data
        feedback.qq = form.qq.data
        feedback.content = form.content.data
        db.session.add(feedback)
    return jsonify(feedback), 201


@api.route('/feedback/lowprice', methods=['POST'])
#@auth.login_required
def create_lowprice_feedback():
    form = LowPriceFeedbackForm.create_api_form()
    with db.auto_commit():
        lowprice_feedback = LowPriceFeedback()
        lowprice_feedback.organization_id = form.organization_id.data
        lowprice_feedback.organization_name = form.organization_name.data
        lowprice_feedback.course_name = form.course_name.data
        lowprice_feedback.name = form.name.data
        lowprice_feedback.phone_num = form.phone_num.data
        db.session.add(lowprice_feedback)
    return jsonify(lowprice_feedback), 201





