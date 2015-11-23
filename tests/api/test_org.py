import json
from herovii.models.org import Org
from tests.api._base import TestOrgCase

__author__ = 'bliss'


class TestOrgInfo(TestOrgCase):
    def test_org_info_updated(self):
        """Org：测试Org基本信息的更新操作"""
        pass

    def test_org_info_created(self):
        """Org：测试Org基本信息的添加操作"""
        uid = 1
        headers = self.get_authorized_header(uid, scope='OrgAdmin')
        org_info = \
            ('北大青鸟', '培训！培训！培训万岁', '武汉市洪山区光谷新世界1602', '武汉',
             '114.421816', '30.498029', '设计培训#精英培训', 1, '0278888888', '无敌#高效')
        org = {
            'name': org_info[0],
            'slogan': org_info[1],
            'location': org_info[2],
            'city': org_info[3],
            'lon': org_info[4],
            'lat': org_info[5],
            'type': org_info[6],
            'audit_status': org_info[7],
            'phone_num': org_info[8],
            'advantage': org_info[9]
        }
        org_json = json.dumps(org)
        print(org_json)
        rv = self.client.post('v1/org', data=org_json, headers=headers)

        print(rv.data)
        self.assertEqual(rv.status_code, 201)

    def test_org_info_query(self):
        pass