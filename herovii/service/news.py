from flask import current_app
from herovii.libs.error_code import NotFound
from herovii.models.news.news_org import NewsOrg

__author__ = 'bliss'


def get_news_org_by_paging(page, count):
    news = NewsOrg.query.filter(NewsOrg.status != -1).order_by(NewsOrg.create_time.desc()). \
        paginate(page, count).items
    total_count = NewsOrg.query.count()
    return total_count, news


def get_news_dto_paginate(page, count):
    total_count, news = get_news_org_by_paging(page, count)
    if news is None:
        raise NotFound(error='news not found', error_code=3000)

    dto_paginate = {
        'news': news,
        'total_count': total_count
    }
    return dto_paginate


def get_org_news_dto_paginate(oid, page, count):
    news = NewsOrg.query(NewsOrg.id, NewsOrg.organization_id, NewsOrg.tag, NewsOrg.title).filter(NewsOrg.status != -1, NewsOrg.organization_id == oid) \
        .order_by(NewsOrg.create_time.desc()). \
        paginate(page, count).items
    total_count = NewsOrg.query.count()
    if news is None:
        raise NotFound(error='news not found', error_code=3000)
    for news_info in news:
        news_info['url'] = current_app.config['SERVER_HOST_NAME'] + '/api.php?s=/organization/noticedetail/id/' + news_info['id']
    dto_paginate = {
        'news': news,
        'total_count': total_count
    }
    return dto_paginate


def get_news_org_by_id(nid):
    news = NewsOrg.query(NewsOrg.id, NewsOrg.organization_id, NewsOrg.tag, NewsOrg.title).filter(NewsOrg.id == nid).first()
    news['url'] = current_app.config['SERVER_HOST_NAME'] + '/api.php?s=/organization/noticedetail/id/' + nid
    return news
