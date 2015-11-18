from herovii.models.news.news_org import NewsOrg

__author__ = 'bliss'


def get_news_org_by_paging(page, count):
    news = NewsOrg.query.paginate(page, count).items
    return news

