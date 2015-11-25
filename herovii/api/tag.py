from flask import json
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.models.tag import Tag

__author__ = 'bliss'

api = ApiBlueprint('tag')


@api.route('/<int:tag_type>')
@auth.login_required
def get_tags(tag_type):
    tags = Tag.query.filter_by(type=tag_type).all()
    json_str = json.dumps(tags)
    return json_str, 200

