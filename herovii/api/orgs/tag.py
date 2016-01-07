from flask import json
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.models.tag import Tag

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/tag/<int:tag_type>')
@auth.login_required
def get_tags(tag_type):
    tags = Tag.query.filter_by(type=tag_type).all()
    json_str = json.dumps(tags)
    headers = {'Content-Type': 'application/json'}
    return json_str, 200, headers

