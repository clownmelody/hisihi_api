__author__ = 'bliss'

from herovii.api.base import ApiBlueprint
from herovii.validator.forms import RegisterForm
from herovii.service import user_srv
from herovii.libs.error_code import NotFound
from herovii.validator import user_verify
from herovii.api.authorization.auth import *

api = ApiBlueprint('user')
# auth = HTTPBasicAuth()


@api.route('', methods=['POST'])
def create_user():
    form = RegisterForm.create_api_form()
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