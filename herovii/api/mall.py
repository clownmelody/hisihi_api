__author__ = 'bliss'

from flask import request, jsonify
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.duiba import DuiBa
from herovii.libs.bpbase import auth


api = ApiBlueprint('mall')


@api.route('/order_duiba', methods=['GET'])
def create_order():
    """兑吧专用扣除积分创建订单接口"""
    duiba = DuiBa()
    success, left_score, bizid = duiba.create_order(request.args.to_dict())

    if success:
        r_data = {
            'status': 'ok',
            'errorMessage': '',
            'bizid': bizid,
            'credits': left_score
         }
        return jsonify(r_data), 200
    else:
        r_error = {
            'status': 'fail',
            'errorMessage': '积分不足',
            'credits': left_score
        }
        return jsonify(r_error), 400

