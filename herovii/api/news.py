from flask import jsonify
from herovii.libs.bpbase import ApiBlueprint
from herovii.libs.error_code import NotFound
from herovii.service.news import get_news_org_by_paging
from herovii.validator.forms import PagingForm

__author__ = 'bliss'

api = ApiBlueprint('news')


@api.route('/org', methods=['GET'])
def list_news():
    form = PagingForm.create_api_form()
    news = get_news_org_by_paging(form.page.data, form.count.data)
    if news is None:
        raise NotFound(error='news not found', error_code=3001)
    return jsonify(news), 200

