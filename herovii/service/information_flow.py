# -*- coding: utf-8 -*-
import json
import urllib
from flask import current_app
from herovii.libs.util import get_oss_pic_path_by_pic_id
from herovii.models.InformationFlow.advs import Advs
from herovii.models.InformationFlow.document import Document
from herovii.models.InformationFlow.document_acticle import DocumentArticle

from herovii.models.InformationFlow.information_flow_banner import InformationFlowBanner
from herovii.models.InformationFlow.information_flow_content import InformationFlowContent
from herovii.models.base import db
from herovii.service.article import is_article_support, is_article_favorite, get_article_support_count

__author__ = 'yangchujie'


# 分页获取资讯流 banner 列表
def get_information_flow_banner_service(page, per_page):
    banner_count = db.session.query(InformationFlowBanner).filter(InformationFlowBanner.status == 1).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    banner_list = db.session.query(InformationFlowBanner) \
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


def get_information_flow_content_service(uid, type, page, per_page):
    content_count = db.session.query(InformationFlowContent).filter(InformationFlowContent.status == 1).count()
    start = (page - 1) * per_page
    stop = start + per_page
    content_list = []
    data_list = db.session.query(InformationFlowContent) \
        .filter(InformationFlowContent.status == 1) \
        .order_by(InformationFlowContent.create_time.desc()) \
        .slice(start, stop) \
        .all()
    if data_list:
        for content in data_list:
            if content.content_type == 1:  # 头条
                info = get_top_content_info_by_id(uid, content.content_id)
            elif content.content_type == 2:  # 视频课程
                info = get_course_info_by_id(content.content_id)
            else:  # 广告图片
                info = get_advs_pic_info_by_id(content.content_id)
            content = {
                'id': content.id,
                'content_type': content.content_type,
                'info': info
            }
            content_list.append(content)
    return content_count, content_list


def get_top_content_info_by_id(uid, article_id):
    """
    {
            "id": "6280",
            "title": "【设计观】设计师为什么总加班？",
            "description": "",
            "view": "6492",
            "create_time": "1457157240",
            "update_time": "1457160887",
            "source_name": "logo大师",
            "logo_pic": "http://hisihi-other.oss-cn-qingdao.aliyuncs.com/2015-12-18/56739c852fdc5.jpg",
            "img": "http://forum-pic.oss-cn-qingdao.aliyuncs.com/2016-03-05/56da82a859ec8.jpg",
            "content_url": "http://hisihi.com/app.php/public/topcontent/version/2.0/type/view/id/6280",
            "share_url": "http://hisihi.com/app.php/public/v2contentforshare/type/view/id/6280/version/2.3",
            "isSupportd": "0",
            "isFavorited": "0",
            "supportCount": 74
        }
    """
    top_content = db.session.query(Document).filter(Document.id == article_id) \
        .first()
    document_article = db.session.query(DocumentArticle).filter(DocumentArticle.id == article_id) \
        .first()
    if top_content:
        content = {
            'id': top_content.id,
            'title': top_content.title,
            'description': top_content.description,
            'img': get_oss_pic_path_by_pic_id(top_content.cover_id, current_app.config['ALI_OSS_FORUM_BUCKET_NAME']),
            'view': top_content.view,
            "content_url": "http://hisihi.com/app.php/public/topcontent/version/2.0/type/view/id/"+str(article_id),
            "share_url": "http://hisihi.com/app.php/public/v2contentforshare/type/view/version/2.3/id/"+str(article_id),
            'create_time': top_content.create_time,
            'update_time': top_content.update_time,
            'isSupportd': is_article_support(uid, article_id),
            'isFavorited': is_article_favorite(uid, article_id),
            'supportCount': get_article_support_count(article_id)
        }
        if document_article:
            content['source_name'] = document_article.source_name
            content['logo_pic'] = get_oss_pic_path_by_pic_id(document_article.logo_pic,
                                                             current_app.config['ALI_OSS_ORG_BUCKET_NAME'])
        return content
    else:
        return None


def get_advs_pic_info_by_id(adv_id):
    """
    {
        "type": "advertisment",
        "pic": "http://advs-pic.oss-cn-qingdao.aliyuncs.com/2016-03-05/56da99210138e.jpg",
        "content_url": "http://hisihi.com/app.php?s=/public/v2contentforshare/version/2.0/type/view/id/6277",
        "title": "如何20分钟白手起家造一个暗月",
        "size": [
            1024,
            400
        ]
    }
    """
    advs = db.session.query(Advs).filter(Advs.id == adv_id) \
        .first()
    if advs:
        advs_info = {
            'type': 'advertisment',
            'content_url': advs.link,
            'title': advs.title
        }
        pic_path = get_oss_pic_path_by_pic_id(advs.advspic_640_960, current_app.config['ALI_OSS_ADV_BUCKET_NAME'])
        advs_info['pic'] = pic_path
        file = urllib.urlopen(pic_path)
        # tmp_image = cStringIO.StringIO(file.read())
        # from tkinter import Image
        # image = Image.open(tmp_image)
        # print(image.size)
        return advs_info
    return None


def get_course_info_by_id(id):
    pass
