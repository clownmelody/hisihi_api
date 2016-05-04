from flask import jsonify, json, request
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.service.overseas_study import get_overseas_study_banner_service
from herovii.validator.forms import PagingForm

__author__ = 'yangchujie'

api = ApiBlueprint('overseas_study')


@api.route('/banner')
#@auth.login_required
def get_overseas_study_banner():
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    count, data = get_overseas_study_banner_service(int(form.page.data), int(form.per_page.data))
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps({"total_count": count, "data":data})
    return json_obj, 200, headers


