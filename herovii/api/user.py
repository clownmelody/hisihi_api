__author__ = 'bliss'

from herovii.validator.forms import RegisterByMobileForm
from herovii.service import user_srv
from herovii.validator import user_verify
from herovii.libs.error_code import NotFound
from herovii.api.token import *
from herovii.models.user_org import UserOrg
from herovii.models.base import db

api = ApiBlueprint('user')
# auth = HTTPBasicAuth()


@api.route('/org', methods=['POST'])
def create_user():
    """ 添加一个机构用户
    :POST:
    {'phone_number':'18699998888', 'sms_code':'876876', 'password':'password'}
    :return:
    """
    form = RegisterByMobileForm.create_api_form()
    valid_data = form.get_valid_data()
    user = account.register_by_email(
        valid_data['username'], valid_data['email'], valid_data['password'])
    return jsonify(user), 201


@api.route('/<uid>', methods=['GET'])
@auth.login_required
def get_user_uid(uid):
    uid = user_verify.verify_uid(uid)
    user = user_srv.get_user_by_uid(uid)
    if user:
        return jsonify(user), 200
    else:
        raise NotFound('user not found', 2000)


@api.route('/test', methods=['GET'])
def test():
    # pass
    user = UserOrg()
    user.password = '19851118'
    user.mobile = "18607131949"
    with db.auto_commit():
        db.session.add(user)
    return jsonify(user), 201
