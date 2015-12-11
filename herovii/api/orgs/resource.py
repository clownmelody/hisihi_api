import datetime
from flask import json, jsonify
from flask.globals import g, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.libs.error_code import IllegalOperation, ParamException, VolumeTooLarge
from herovii.models.base import db
from herovii.models.org.info import Info
from herovii.models.org.pic import Pic
from herovii.models.org.qrcode import QrcodeSignIn
from herovii.service.org import create_org_pics
from herovii.validator.forms import OrgPicForm

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/<int:oid>/pics', methods=['POST'])
@auth.login_required
def upload_pic(oid):
    org_info = Info.query.filter_by(uid=g.user[0]).first()

    if org_info.id != oid:
        raise IllegalOperation()
    temp_pics = request.get_json(silent=True, force=True)
    if not temp_pics:
        raise ParamException()
    if len(temp_pics) >= 20:
        raise VolumeTooLarge()

    pics = []
    for temp_pic in temp_pics:
        OrgPicForm.create_api_form(self_data=temp_pic)
        temp_pic['organization_id'] = oid
        pic = Pic()
        for key, value in temp_pic.items():
            setattr(pic, key, value)
        pics.append(pic)
    r_pics = create_org_pics(pics)
    str_data = json.dumps(r_pics)
    headers = {'Content-Type': 'application/json'}
    return str_data, 201, headers


@api.route('/<int:oid>/qrcode/sign-in/today', methods=['POST'])
# @auth.login_required
def get_qrcode_sign_in_today(oid):
    today = datetime.datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    qrcode = QrcodeSignIn.query.filter_by(
        organization_id=oid, date=date_str).first()
    if qrcode:
        return jsonify(qrcode), 201
    qrcode = QrcodeSignIn(oid, today)
    qrcode.make()
    with db.auto_commit():
        db.session.add(qrcode)
    return jsonify(qrcode), 201

