__author__ = 'bliss'


from ._base import TestCase
from herovii.libs.httper import Httper


class TestMall(TestCase):
    def test_redirect_to_duiba(self):
        headers = self.get_authorized_header()
        rv = self.client.get('/v1/mall/duiba/index', headers=headers)
        http = Httper()
        r_redirect = http.get(rv.location)

        print(r_redirect.status)
        assert r_redirect.status == 200

