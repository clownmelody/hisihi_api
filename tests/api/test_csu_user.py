from flask import json, jsonify
from herovii.models.user.user_csu_secure import UserCSUSecure
from tests.api._base import  TestUserCSUCase

__author__ = 'bliss'


class TestUserCSU(TestUserCSUCase):
    def test_password_md5(self):
        """消费用户：密码加密是否符合预期"""
        user = UserCSUSecure.query.filter_by(id=2).first()

        # 1122333 密码加密后应该为下面的数值
        should_be = '7c3307fac7459f1cd889810bdbb3e683'
        self.assertEqual(user.password, should_be)

    def test_csu_query(self):
        headers = self.get_authorized_header()

        get_param = '?mobile=18888888888'
        rv = self.client.get('v1/user/csu' + get_param, headers=headers)
        self.assertEqual(200, rv.status_code)

    def test_user_identity_change(self):
        headers = self.get_authorized_header()
        data = {
            'uid': 1,
            'group_id': 2
        }
        data_json = json.dumps(data)
        rv = self.client.put('v1/user/csu/indentity', data=data_json)
        self.assertEqual(rv.status_code, 202)
