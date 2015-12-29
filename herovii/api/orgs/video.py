from flask import jsonify
from herovii.libs.bpbase import ApiBlueprint
from herovii.models.base import db
from herovii.models.org.video import Video
from herovii.validator.forms import VideoUpdateForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/pic')
def update_video():
    form = VideoUpdateForm.create_api_form()
    course = Video.query.filter_by(id=form.id.data).first_or_404()
    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(course, key, value)
    return jsonify(course), 202


