__author__ = 'bliss'

from herovii.libs.bpbase import ApiBlueprint
from herovii.models.onlines.online import Online
from herovii.models.onlines.statistic import Statistic
from herovii.models.base import db

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


