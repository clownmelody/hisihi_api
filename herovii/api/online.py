__author__ = 'bliss'

from herovii.libs.bpbase import ApiBlueprint
from herovii.models.onlines.online import Online
from herovii.models.onlines.statistic import Statistic
from herovii.models.base import db
from herovii.validator.forms import OnlineIDForm
from herovii.service.online import pv_added_1, share_added_1
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
    form = OnlineIDForm().create_api_form()
    count = pv_added_1(form.oid.data)
    if count >= 1:
        return success_json(), 202
    else:
        raise UnknownError()


@api.route('share+1', methods=['PUT'])
def share_plus_1():
    """ 分享次数+1
    :PUT:
        sample: {"oid" : 1}
    :return:
    """
    form = OnlineIDForm().create_api_form()
    count = share_added_1(form.oid.data)
    if count >= 1:
        return success_json(), 202
    else:
        raise UnknownError()


