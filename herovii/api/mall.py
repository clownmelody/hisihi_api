__author__ = 'bliss'

from flask import request, jsonify, g, redirect
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.duiba import DuiBa
from herovii.libs.bpbase import auth
from herovii.models.user.user_csu import UserCSU


api = ApiBlueprint('mall')


@api.route('/duiba/order', methods=['GET'])
def create_order_duiba():
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


@api.route('/duiba/firm', methods=['GET'])
def firm_order_duiba():
    """兑吧专用接口，返回兑换是否成功
    如果没有返回 ok ，兑吧要调用此接口5次？"""
    duiba = DuiBa()
    flag = duiba.confirm_order(request.args.to_dict())
    if flag == 'ok':
        return flag, 200
    else:
        return flag, 400


@api.route('/duiba/index', methods=['GET'])
@auth.login_required
def redirect_to_duiba():
    """将用户重定向到兑吧的商城中
    http://www.duiba.com.cn/autoLogin/autologin?uid=test001&
    credits=100&appKey=jlg88loSQobWDMmGrPLqtmr&sign=fbce303d7ba7ca7b0fe14d576b494769&
    timestamp=1418625055000
    """
    user_info = g.user
    uid = user_info[0]
    user_csu = UserCSU.query.get(uid)
    duiba = DuiBa()
    login_url = duiba.create_login_url(uid, user_csu.score)
    return redirect(login_url)

