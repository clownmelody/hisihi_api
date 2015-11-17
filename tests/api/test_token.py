__author__ = 'bliss'

import json, time
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

    def test_token_expired(self):
        headers = self.get_authorized_header(expiration=1)
        time.sleep(3)
        rv = self.client.get('/v1/test/auth', headers=headers)
        print(rv.data)
        assert rv.status_code == 401
        assert b'1003' in rv.data


