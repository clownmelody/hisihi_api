

from herovii.libs.error_code import NotFound
from herovii.libs.helper import success_json
from herovii.models.base import db
from flask import jsonify, json, request, redirect
from herovii.libs.bpbase import ApiBlueprint, auth
from herovii.models.org.university_enroll import UniversityEnroll
from herovii.models.overseas.overseas_plan import OverseasPlan
from herovii.service.overseas_study import get_overseas_study_banner_service, get_overseas_study_hot_country_service, \
    get_overseas_study_hot_university_service, get_overseas_study_university_info_service, \
    get_overseas_study_university_list_by_country_id_service, get_overseas_study_country_service, \
    get_overseas_study_university_photos_service, get_overseas_study_university_majors_service,\
    get_overseas_study_university_list_service, put_overseas_article_service,\
    get_org_overseas_plan_list_service, get_org_overseas_plan_detail_service, get_org_overseas_plan_text_service
from herovii.validator.forms import PagingForm, OrgUniversityEnrollForm, OverseaPlanUpdateForm, OverseaPlanAddForm, \
    OverseaPlanForm

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


@api.route('/hot_country')
#@auth.login_required
def get_overseas_study_hot_country():
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    if page == 0:
        page = 1
    if per_page == 0:
        per_page = 8
    count, data = get_overseas_study_hot_country_service(page, per_page)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps({"total_count": count, "data": data})
    return json_obj, 200, headers


@api.route('/country')
#@auth.login_required
def get_overseas_study_country():
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    count, data = get_overseas_study_country_service(page, per_page)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps({"total_count": count, "data": data})
    return json_obj, 200, headers


@api.route('/hot_university')
#@auth.login_required
def get_overseas_study_hot_university():
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    if page == 0:
        page = 1
    if per_page == 0:
        per_page = 8
    count, data = get_overseas_study_hot_university_service(page, per_page)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps({"total_count": count, "data": data})
    return json_obj, 200, headers


@api.route('/university/<int:uid>', methods=['GET'])
#@auth.login_required
def get_overseas_study_university_info(uid):
    data = get_overseas_study_university_info_service(uid)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps(data)
    return json_obj, 200, headers


@api.route('/country/<int:cid>/university', methods=['GET'])
#@auth.login_required
def get_overseas_study_university_list_by_country_id(cid):
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    count, data = get_overseas_study_university_list_by_country_id_service(cid, page, per_page)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps({"total_count": count, "data": data})
    return json_obj, 200, headers


@api.route('/university/<int:uid>/photos', methods=['GET'])
#@auth.login_required
def get_overseas_study_university_photos(uid):
    args = request.args.to_dict()
    form = PagingForm.create_api_form(**args)
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    data = get_overseas_study_university_photos_service(uid, page, per_page)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps(data)
    return json_obj, 200, headers


@api.route('/university/enroll', methods=['POST'])
@auth.login_required
def create_university_enroll():
    form = OrgUniversityEnrollForm.create_api_form()
    university_enroll = UniversityEnroll()
    for key, value in form.body_data.items():
        setattr(university_enroll, key, value)
    with db.auto_commit():
        db.session.add(university_enroll)
    return jsonify(university_enroll), 201


@api.route('/university/<int:uid>/majors', methods=['GET'])
#@auth.login_required
def get_overseas_study_university_majors(uid):
    data = get_overseas_study_university_majors_service(uid)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps(data)
    return json_obj, 200, headers


@api.route('/universities', methods=['GET'])
#@auth.login_required
def get_overseas_study_university_list():
    data = get_overseas_study_university_list_service()
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps({"total_count": len(data), "data": data})
    return json_obj, 200, headers


@api.route('/plan', methods=['POST'])
@auth.login_required
def put_overseas_article():
    form = OverseaPlanAddForm().create_api_form()
    text = form.html_content.data
    url = form.url.data
    oid = form.oid.data
    data = put_overseas_article_service(oid, text, url)
    return jsonify(data), 201


@api.route('/org/<int:oid>/plans', methods=['GET'])
@auth.login_required
def get_org_overseas_plan_list(oid):
    data = get_org_overseas_plan_list_service(oid)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps({"total_count": len(data), "data": data})
    return json_obj, 200, headers


@api.route('/plans/<int:pid>', methods=['GET'])
@auth.login_required
def get_org_overseas_plan_detail(pid):
    data = get_org_overseas_plan_detail_service(pid)
    headers = {'Content-Type': 'application/json'}
    json_obj = json.dumps(data)
    return json_obj, 200, headers


@api.route('/plans/<int:pid>', methods=['PUT'])
@auth.login_required
def update_org_overseas_plan_detail(pid):
    form = OverseaPlanUpdateForm().create_api_form()
    plan_info = OverseasPlan.query.get(pid)
    if not plan_info:
        raise NotFound(error='overseas plan not found')
    with db.auto_commit():
        for key, value in form.body_data.items():
            setattr(plan_info, key, value)
    return jsonify(plan_info), 202


@api.route('/plan/index', methods=['POST'])
def redirect_to_plan():
    """
    重定向到机构留学计划
    """
    json_url = request.get_json(force=True)
    id = json_url['id']
    url = json_url['url']
    return redirect(url, 301)


@api.route('/plan/<int:pid>', methods=['DELETE'])
@auth.login_required
def delete_org_overseas_plan_detail(pid):
    with db.auto_commit():
        db.session.query(OverseasPlan).filter(OverseasPlan.id == pid) \
            .update({OverseasPlan.status: -1})
    return success_json(), 204


@api.route('/plan/text', methods=['POST'])
@auth.login_required
def get_org_overseas_plan_text():
    json_url = request.get_json(force=True)
    flag = json_url['flag']
    plans = json_url['plans']
    text_list = get_org_overseas_plan_text_service(flag, plans)
    data = {
        'text_list': text_list
    }
    return jsonify(data), 200

