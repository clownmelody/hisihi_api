__author__ = 'bliss'

from flask import request, jsonify
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.duiba import DuiBa
from herovii.libs.bpbase import auth


api = ApiBlueprint('mall')


@api.route('/order', methods=['POST'])
def create_order():
    uid = request.args.get('uid')
    credit = request.args.get('credits')
    duiba = DuiBa()
    order = duiba.create_order(request.args.to_dict())
    r_data = {
        'status': 'ok',
        'errorMessage': '',
        'bizid': '20140730192133033',
        'credits': '100'
    }
    if order is not None:
        return jsonify(r_data), 200
    else:
        r_error = {
            'status': 'fail',
            'errorMessage': '失败原因（显示给用户）',
            'credits': '100'
        }
        return jsonify(r_error), 400

