from tests.api._base import TestNewsOrgCase

__author__ = 'bliss'

import unittest
from ._base import TestCase


class TestOrgNews(TestNewsOrgCase):
    def test_org_news_paging(self):
        url = '/v1/news/org?page=1&count=2'
        rv = self.client.get(url)
        print(rv.data)
        self.assertEqual(rv.status_code, 200)


