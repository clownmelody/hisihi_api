# -*- coding: utf-8 -*-
import datetime
import json
import urllib.request
from flask import current_app
from sqlalchemy import func
from herovii.libs.util import get_oss_pic_path_by_pic_id, get_img_service_path_by_pic_id
from herovii.models.InformationFlow.advs import Advs
from herovii.models.InformationFlow.document import Document
from herovii.models.InformationFlow.document_acticle import DocumentArticle

from herovii.models.InformationFlow.information_flow_banner import InformationFlowBanner
from herovii.models.InformationFlow.information_flow_config import InformationFlowConfig
from herovii.models.InformationFlow.information_flow_content import InformationFlowContent
from herovii.models.base import db
from herovii.models.issue import Issue
from herovii.models.org.course import Course
from herovii.models.org.video import Video
from herovii.service.article import is_article_support, is_article_favorite, get_article_support_count
from herovii.service.org import get_organization_info_by_organization_id, get_user_profile_by_uid

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


def get_information_flow_content_service(uid, config_type, page, per_page):
    start = (page - 1) * per_page
    stop = start + per_page
    content_list = []
    if config_type == 0:
        content_count = db.session.query(InformationFlowContent).filter(InformationFlowContent.status == 1).count()
        data_list = db.session.query(InformationFlowContent) \
            .filter(InformationFlowContent.status == 1) \
            .order_by(InformationFlowContent.create_time.desc()) \
            .slice(start, stop) \
            .all()
    else:
        content_count = db.session.query(InformationFlowContent).filter(InformationFlowContent.status == 1,
                                                                        InformationFlowContent.config_type == config_type) \
            .count()
        data_list = db.session.query(InformationFlowContent) \
            .filter(InformationFlowContent.status == 1,
                    InformationFlowContent.config_type == config_type) \
            .order_by(InformationFlowContent.create_time.desc()) \
            .slice(start, stop) \
            .all()
    if data_list:
        for content in data_list:
            info_content = {
                'id': content.id,
                'content_type': content.content_type
            }
            if content.content_type == 1:  # 头条
                info = get_top_content_info_by_id(uid, content.content_id)
                info_content['top_content_info'] = info
            elif content.content_type == 2:  # 视频课程
                info = get_course_info_by_id(content.content_id)
                info_content['course_info'] = info
            else:  # 广告图片
                info = get_advs_pic_info_by_id(content.content_id)
                info_content['adv_info'] = info
            content_list.append(info_content)
    return content_count, content_list


def get_top_content_info_by_id(uid, article_id):
    """
    根据 id 获取头条信息
    :param uid:   用户 id
    :param article_id:  头条 id
    :return:
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
            "content_url": "http://hisihi.com/app.php/public/topcontent/version/2.0/type/view/id/" + str(article_id),
            "share_url": "http://hisihi.com/app.php/public/v2contentforshare/type/view/version/2.3/id/" + str(
                article_id),
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
    根据 id 获取广告图片信息
    :param adv_id: 广告 id
    :return:
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
        img_service_path = get_img_service_path_by_pic_id(advs.advspic_640_960,
                                                          current_app.config['ALI_OSS_ADV_BUCKET_NAME'])
        resp = urllib.request.urlopen(img_service_path)
        resp_dict = json.loads(str(resp.read(), encoding="utf-8"))
        advs_info['size'] = [resp_dict['width'], resp_dict['height']]
        return advs_info
    return None


def get_course_info_by_id(course_id):
    """
    根据 course_id 获取视频课程信息
    :param course_id: 课程 id
    :return:
        {
            "id":"46",
            "title":"钢铁侠教你如何制杖",
            "lecturer":"103",
            "ViewCount":"36377",
            "type":"平面设计",
            "lecturer_name":"皮卡Q",
            "img":"http://pic.hisihi.com/2016-02-29/1456726581454771.jpg",
            "organization_logo":"http://pic.hisihi.com/2016-02-29/1456727795774772.jpg@13-13-355-355a",
            "duration":"235"
        }
    """
    organization_course = db.session.query(Course).filter(Course.id == course_id) \
        .first()
    organization_info = get_organization_info_by_organization_id(organization_course.organization_id)
    if organization_course:
        lecturer_id = organization_course['lecturer']
        user_profile = get_user_profile_by_uid(lecturer_id)
        if user_profile is not None:
            lecturer_nickname = user_profile['nickname']
        else:
            lecturer_nickname = ''
        type_str = get_course_type_name_by_type_id(organization_course['category_id'])
        duration = get_course_video_duration(course_id)
        img_str = parse_img_str(organization_course['img_str'])
        course = {
            'id': course_id,
            'title': organization_course['title'],
            'lecturer': lecturer_id,
            'ViewCount': organization_course['view_count'],
            'type': type_str,
            'img': img_str,
            'lecturer_name': lecturer_nickname,
            'organization_logo': organization_info['logo'],
            'duration': duration
        }
        return course
    else:
        return None


def get_course_type_name_by_type_id(type_id):
    """
    通过类别 id 获取课程类型名字
    :param type_id:
    :return:
    """
    issue = db.session.query(Issue).filter(Issue.id == type_id) \
        .first()
    if issue:
        return issue['title']
    else:
        return None


def get_course_video_duration(course_id):
    """
    通过课程 id 获取课程时长
    :param course_id:
    :return:
    """
    data_list = db.session.query(Video) \
        .filter(Video.course_id == course_id,
                Video.status == 1) \
        .all()
    course_duration = 0
    if data_list:
        for content in data_list:
            course_duration = course_duration + content.duration
    return course_duration


def get_information_flow_content_type_service():
    data_list = []
    config_list = db.session.query(InformationFlowConfig) \
        .filter(InformationFlowConfig.status == 1) \
        .all()
    if config_list:
        for config in config_list:
            config_object = {
                'id': config.id,
                'title': config.title
            }
            data_list.append(config_object)
    return len(data_list), data_list


def parse_img_str(img_str):
    if img_str.startswith('http'):
        return img_str
    else:
        url_prefix = 'http://game-pic.oss-cn-qingdao.aliyuncs.com/'
        return url_prefix + img_str[4:]
