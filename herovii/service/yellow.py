from sqlalchemy import func

from herovii.libs.error_code import NotFound
from herovii.models.yellowpages.pageclass import Category
from herovii.models.yellowpages.yellowpages import Yellow
from herovii.models.yellowpages.yellowpageslabel import YellowLabel
from herovii.models.base import db
__author__ = 'melody'


def get_yellow_pages():
    count_by_category = db.session.query(func.count(Category.id).label('count'), Category.id)\
        .join(Yellow, Yellow.class_id == Category.id)\
        .filter(Yellow.status >= 1)\
        .group_by(Category.id)\
        .all()
    sites = db.session.query(Category.id, Yellow.class_id, Yellow.website_name.label('site_name'),
                             Yellow.icon_url.label('site_logo'),
                             Yellow.url.label('site_url'), YellowLabel.url.label('icon'))\
        .join(Yellow, Category.id == Yellow.class_id)\
        .outerjoin(YellowLabel, Yellow.label == YellowLabel.id)\
        .filter(Yellow.status >= 1)\
        .all()
    category = db.session.query(Category.id, Category.category_name, Category.icon_url.label('category_icon'))\
        .filter(Category.status != -1).all()
    category_count = Category.query.filter(Category.status != -1).count()
    return sites, count_by_category, category, category_count


def get_yellow_pages_list():
    sites, count_by_category, category, category_count = get_yellow_pages()

    if sites is None:
        raise NotFound(error='sites not found', error_code=3000)
    if category is None:
        raise NotFound(error='classes not found', error_code=3000)
    json_sites = {
        'total_count': category_count,
        'data': []
    }
    for i in range(0, len(category)):
        json_sites['data'].append(
            {
                'category_name': category[i].category_name,
                'category_icon': category[i].category_icon,
                'count': 0,
                'data': []
            }
        )
        for category_count_item in count_by_category:
            if category[i].id == category_count_item.id:
                json_sites['data'][i]['count'] = category_count_item.count
        for site_item in sites:
            if site_item.class_id == category[i].id:
                json_sites['data'][i]['data'].append(
                    {
                        'site_logo': site_item.site_logo,
                        'site_name': site_item.site_name,
                        'site_url': site_item.site_url,
                        'icon': site_item.icon
                    }
                )
    return json_sites


def get_recommend_sites():
    recommend = db.session.query(Yellow.icon_url.label('site_logo'), Yellow.url.label('site_url'),
                                 Yellow.website_name.label('site_name'), YellowLabel.url.label('icon'))\
        .outerjoin(YellowLabel, Yellow.label == YellowLabel.id)\
        .filter(Yellow.status == 2).all()
    count = db.session.query(Yellow).filter(Yellow.status == 2).count()
    if recommend is None:
        raise NotFound(error='recommend_sites not found', error_code=3000)

    json_recommend = {
        'total_count': count,
        'data': []
    }
    for i in range(0, len(recommend)):
        json_recommend['data'].append(
            {
                'site_logo': recommend[i].site_logo,
                'site_name': recommend[i].site_name,
                'site_url': recommend[i].site_url,
                'icon': recommend[i].icon
            }
        )
    return json_recommend
