# -*- coding: utf-8 -*-

from herovii.models.InformationFlowBanner.information_flow_banner import InformationFlowBanner
from herovii.models.base import db

__author__ = 'yangchujie'


# 分页获取资讯流 banner 列表
def get_information_flow_banner_service(page, per_page):
    banner_count = db.session.query(InformationFlowBanner).filter(InformationFlowBanner.status == 1).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    banner_list = db.session.query(InformationFlowBanner)\
        .filter(InformationFlowBanner.status == 1) \
        .slice(start, stop) \
        .all()
    if banner_list:
        for banner in banner_list:
            banner_object = {
                'id': banner.id,
                'pic_url': banner.pic_url,
                'url': banner.url
            }
            data_list.append(banner_object)
    return banner_count, data_list




