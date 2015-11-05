__author__ = 'bliss'

from flask import json, jsonify, request
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.helper import android_ipad_iphone
from herovii.models.onlines.online import Online
from herovii.models.onlines.statistic import Statistic
from herovii.models.base import db
from herovii.service.statistic import downloads_plus_1 as added

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


def pv_plus_1():
    pass


@api.route('/<oid>/downloads-added', methods=['GET'])
def downloads_plus_1(oid):
    r = request.remote_addr
    head_agent = request.user_agent.string
    type = android_ipad_iphone(head_agent)
    added(oid, type)
    pass


def finished_plus_1():
    pass


def uv_plus_1():
    pass