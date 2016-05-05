# -*- coding: utf-8 -*-
from herovii import db
from herovii.models.InformationFlow.information_flow_banner import InformationFlowBanner
from herovii.models.overseas.country import Country

__author__ = 'yangchujie'


def get_overseas_study_banner_service(page, per_page):
    banner_count = db.session.query(InformationFlowBanner).filter(InformationFlowBanner.status == 1,
                                                                  InformationFlowBanner.show_pos == 3).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    banner_list = db.session.query(InformationFlowBanner) \
        .filter(InformationFlowBanner.status == 1,
                InformationFlowBanner.show_pos == 3) \
        .slice(start, stop) \
        .all()
    if banner_list:
        for banner in banner_list:
            jump_type = banner.jump_type
            banner_object = {
                'id': banner.id,
                'pic_url': banner.pic_url,
                'jump_type': jump_type,
                'url': banner.url
            }
            if jump_type == 2:
                post_id = banner.url
                banner_object['url'] = 'hisihi://post/detailinfo?id=' + post_id
            elif jump_type == 3:
                course_id = banner.url
                banner_object['url'] = 'hisihi://course/detailinfo?id=' + course_id
            elif jump_type == 4:
                org_id = banner.url
                banner_object['url'] = 'hisihi://organization/detailinfo?id=' + org_id
            elif jump_type == 5:
                university_id = banner.url
                banner_object['url'] = 'hisihi://university/detailinfo?id=' + university_id
            data_list.append(banner_object)
    return banner_count, data_list


def get_overseas_study_hot_country_service(page, per_page):
    country_count = db.session.query(Country).filter(Country.status == 1,
                                                     Country.is_hot == 1).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    country_list = db.session.query(Country.id, Country.name, Country.logo_url) \
        .filter(Country.status == 1,
                Country.is_hot == 1) \
        .slice(start, stop) \
        .all()
    for country in country_list:
        data = {
            'id': country.id,
            'name': country.name,
            'logo_url': country.logo_url
        }
        data_list.append(data)
    return country_count, data_list
