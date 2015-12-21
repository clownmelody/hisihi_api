from tests.api._base import TestOrgCase
from flask import json
__author__ = 'shaolei'


class TestFeedback(TestOrgCase):

    def test_feedback_add(self):
        feedback_info = {
            'organization_id': 2,
            'admin_id': 3,
            'qq': '1173838760',
            'content': '闪退'
        }
        feedback_json = json.dumps(feedback_info)
        rv = self.client.post('v1/org/feedback/post', data=feedback_json)
        self.assertEqual(rv.status_code, 201)
