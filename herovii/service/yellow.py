
from herovii.libs.error_code import NotFound
from herovii.models.yellowpages.pageclass import Category
from herovii.models.yellowpages.yellowpages import Yellow

__author__ = 'melody'


def get_yellow_pages_by_paging(page, per_page):
    sites = Yellow.query.filter(Yellow.status != -1).paginate(page, per_page).items
    total_count = Yellow.query.count()
    category = Category.query.filter(Category.status != -1, Category.id == sites.class_id).items

    return sites, total_count, category


def get_yellow_pages_list(page, per_page):
    sites, total_count, category = get_yellow_pages_by_paging(page, per_page)

    if sites is None:
        raise NotFound(error='sites not found', error_code=3000)
    if category is None:
        raise NotFound(error='classes not found', error_code=3000)

    json_sites = {
        'total_count': total_count,
        'content': [
            {
                'name': category.category_name,
                'icon_url': category.icon_url,
                'yellow_pages': [
                    {
                        'web_name': sites.web_name,
                        'url': sites.url,
                        'icon_url': sites.icon_url
                    }
                ]
            }
        ]
    }

    return json_sites


def get_recommend_sites():
    recommend = Yellow.query.filter(Yellow.status != -1, Yellow.state == 2).items
    if recommend is None:
        raise NotFound(error='recommendSites not found', error_code=3000)

    json_recommend = {
        'web_name': recommend.web_name,
        'url': recommend.url,
        'icon_url': recommend.icon_url,
    }

    return json_recommend
