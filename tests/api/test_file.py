import json
from tests.api._base import TestCase

__author__ = 'bliss'


class TestFile(TestCase):
    def test_create_qrcode(self):
        data = {
            "url": "http://sina.com"
        }
        json_str = json.dumps(data)
        rv = self.client.post('v1/file/qrcode', data=json_str)
        self.assertEqual(rv.status_code, 201)
