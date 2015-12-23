from flask import json
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.models.issue import Issue

__author__ = 'bliss'


api = ApiBlueprint('tag')


@api.route('/issues/lv1')
@auth.login_required
def get_tags():
    tags = Issue.query.filter_by(status=1, pid=0, status=1).all()
    json_str = json.dumps(tags)
    headers = {'Content-Type': 'application/json'}
    return json_str, 200, headers

