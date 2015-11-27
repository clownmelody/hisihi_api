from flask import json
from tests.api._base import TestOrgCase

__author__ = 'bliss'


class TestOrg(TestOrgCase):
    def test_org_info_updated(self):
        """OrgInfo：测试Org基本信息的更新操作"""
        org_info = {
            'id': 1,
            'name': '名字被改变',
            'introduce': '新增名字'
        }
        headers = self.get_authorized_header(2, scope='OrgAdmin')
        org_json = json.dumps(org_info)
        rv = self.client.put('v1/org', data=org_json, headers=headers)
        self.assertEqual(rv.status_code, 403)

        headers = self.get_authorized_header(1, scope='OrgAdmin')
        rv = self.client.put('v1/org', data=org_json, headers=headers)
        self.assertEqual(rv.status_code, 202)

    def test_org_info_created(self):
        """OrgInfo：测试Org基本信息的添加操作"""
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
        rv = self.client.post('v1/org', data=org_json, headers=headers)

        self.assertEqual(rv.status_code, 201)

    def test_org_info_query(self):
        oid = '2'
        headers = self.get_authorized_header(2, scope='OrgAdmin')
        rv = self.client.get('v1/org/'+oid, headers=headers)
        print(type(rv.data))
        self.assertEqual(rv.status_code, 200)
        json_obj = json.loads(rv.data)
        print(json_obj)
        self.assertEqual(json_obj['id'], 2)

        oid = '-1'
        rv = self.client.get('v1/org' + oid, headers=headers)
        self.assertEqual(rv.status_code, 404)

    def test_org_pics_create(self):
        oid = '1'
        headers = self.get_authorized_header(1, scope='OrgAdmin')
        data = [
            {
                'url': 'http://321.com',
                'type': 1,
                'description': 'this is for test'
            },
            {
                'url': 'http://321.com',
                'type': 2,
                'description': 'this is for test'
            }
        ]
        data_str = json.dumps(data)
        rv = self.client.post('v1/org/' + oid + '/pics',
                              data=data_str, headers=headers)
        self.assertEqual(rv.status_code, 201)

