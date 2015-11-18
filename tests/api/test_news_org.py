from tests.api._base import TestNewsOrgCase

__author__ = 'bliss'


class TestOrgNews(TestNewsOrgCase):
    def test_org_news_paging(self):
        """News：对Org的新闻查新接口做测试"""
        url = '/v1/news/org?page=1&count=2'
        rv = self.client.get(url)
        self.assertEqual(rv.status_code, 200)