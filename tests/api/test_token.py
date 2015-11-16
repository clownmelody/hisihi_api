__author__ = 'bliss'

import json
from ._base import TestCase


class TestToken(TestCase):
    def test_get_token(self):
        data = json.dumps({
            'account': 'aswind',
            'secret': '123123',
            'type': '200'
        })

        rv = self.client.post('/v1/token', data=data)
        assert rv.status_code == 201
