__author__ = 'bliss'

from flask import request, jsonify
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.bpbase import auth


api = ApiBlueprint('credit')


@api.route('/deduct')
def deduct_credit():
    uid = request.args.get('uid')
    credit = request.args.get('credits')
    r_data = {
        'status': 'ok',
        'errorMessage': '',
        'bizid': '20140730192133033',
        'credits': '100'
    }
    return jsonify(r_data), 200

