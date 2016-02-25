from herovii.libs.error_code import NotFound
from herovii.models.yellowpages.pageclass import Category
from herovii.models.yellowpages.yellowpages import Yellow

__author__ = 'melody'


def get_yellow_pages():
    sites = Yellow.query.filter(Yellow.status != -1).all()
    total_count = Yellow.query.count()
    category = Category.query.filter(Category.status != -1).all()

    return sites, total_count, category


def get_yellow_pages_list():
    sites, total_count, category = get_yellow_pages()

    if sites is None:
        raise NotFound(error='sites not found', error_code=3000)
    if category is None:
        raise NotFound(error='classes not found', error_code=3000)

    class_oid = []
    for i in range(0, len(sites)):
        class_oid.append(sites[i].class_id)
    class_oid = list(set(class_oid))

    need_category = []
    for i in range(0, len(category)):
        for t in range(0, len(class_oid)):
            if category[i].id == class_oid[t]:
                need_category.append(category[i])

    json_sites = {
        'total_count': total_count,
        'content': []
    }

    for i in range(0, len(need_category)):
        json_sites['content'].append(
            {
                'name': need_category[i].category_name,
                'icon_url': need_category[i].icon_url,
                'yellow_pages': []
            }
        )

    for i in range(0, len(need_category)):
        for t in range(0, len(sites)):
            if sites[t].class_id == need_category[i].id:
                json_sites['content'][i]['yellow_pages'].append(
                    {
                        'web_name': sites[t].web_name,
                        'url': sites[t].url,
                        'icon_url': sites[t].icon_url
                    }
                )

    return json_sites


def get_recommend_sites():
    recommend = Yellow.query.filter(Yellow.status != -1, Yellow.state == 2).all()
    if recommend is None:
        raise NotFound(error='recommend_sites not found', error_code=3000)

    json_recommend = []
    for i in range(0, len(recommend)):
        json_recommend.append(
            {
                'web_name': recommend[i].web_name,
                'url': recommend[i].url,
                'icon_url': recommend[i].icon_url
            }
        )

    return json_recommend
