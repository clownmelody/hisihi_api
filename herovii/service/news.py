from flask import current_app
from herovii import db
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


def get_org_news_dto_paginate(oid, page, per_page):
    start = (page - 1) * per_page
    stop = start + per_page
    news = db.session.query(NewsOrg.id, NewsOrg.organization_id, NewsOrg.title, NewsOrg.tag).filter(
        NewsOrg.status != -1, NewsOrg.organization_id == oid) \
        .order_by(NewsOrg.create_time.desc()) \
        .slice(start, stop) \
        .all()
    total_count = NewsOrg.query.count()
    data_list = []
    if news is None:
        raise NotFound(error='news not found', error_code=3000)
    for news_info in news:
        data = {
            'id': news_info.id,
            'organization_id': news_info.organization_id,
            'tag': news_info.tag,
            'title': news_info.title,
            'url': current_app.config['SERVER_HOST_NAME'] + '/api.php?s=/organization/noticedetail/id/'+str(news_info.id)
        }
        data_list.append(data)
    dto_paginate = {
        'news': data_list,
        'total_count': total_count
    }
    return dto_paginate


def get_news_org_by_id(nid):
    news = db.session.query(NewsOrg.id, NewsOrg.organization_id, NewsOrg.title, NewsOrg.tag).filter(
        NewsOrg.id == nid).first()
    return {
            'id': news.id,
            'organization_id': news.organization_id,
            'tag': news.tag,
            'title': news.title,
            'url': current_app.config['SERVER_HOST_NAME'] + '/api.php?s=/organization/noticedetail/id/'+str(news.id)
        }
