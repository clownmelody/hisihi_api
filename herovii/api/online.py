__author__ = 'bliss'

from herovii.libs.bpbase import ApiBlueprint
from herovii.models.onlines.online import Online
from herovii.models.onlines.statistic import Statistic
from herovii.models.base import db
from herovii.validator.forms import PVPlus1ByOnlineForm
from herovii.service.online import pv_plus_1 as pv_added
from herovii.libs.helper import success_json
from herovii.libs.error_code import UnknownError

api = ApiBlueprint('online')


@api.route('', methods=['GET'])
def create_online():
    online = Online()
    online.title = '光棍节找妹子啦'
    static = Statistic()
    with db.auto_commit():
        db.session.add(online)
    static.f_online_id = online.id
    with db.auto_commit():
        db.session.add(static)
    return 'success', 201


@api.route('/pv+1', methods=['PUT'])
def pv_plus_1():
    """ 活动页面浏览量+1
    :PUT:
        sample: {"oid":1}
    :return:
    """
    form = PVPlus1ByOnlineForm().create_api_form()
    count = pv_added(form.oid.data)
    if count >= 1:
        return success_json(), 202
    else:
        raise UnknownError()


@api.route('/finished+1', methods=['PUT'])
def finished_plus_1():
    """ 完整参与活动数量+1
    :PUT:

    :return:
    """


def uv_plus_1():
    pass


