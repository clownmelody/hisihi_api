# -*- coding: utf-8 -*-
from flask import current_app
from herovii import db
from herovii.libs.error_code import NotFound
from herovii.models.forum.TopicToPostRelation import TopicToPostRelation
from herovii.models.forum.topic import Topic
from herovii.models.user.follow import Follow

__author__ = 'yangchujie'


def get_forum_hot_topic_list_service():
    count = db.session.query(Topic).filter(Topic.status == 1,
                                           Topic.is_hot == 1) \
        .count()
    topic_list = db.session.query(Topic).filter(Topic.status == 1,
                                                Topic.is_hot == 1) \
        .order_by(Topic.sort.asc(), Topic.create_time.desc()) \
        .all()
    data_list = []
    for topic in topic_list:
        info = {
            'id': topic.id,
            'title': topic.title,
            'description': topic.description,
            'img_url': topic.img_url,
            'is_hot': topic.is_hot,
            'post_count': get_post_count_by_topic_id(topic.id)
        }
        data_list.append(info)
    return count, data_list


def get_forum_common_topic_list_service(page, per_page):
    count = db.session.query(Topic).filter(Topic.status == 1,
                                           Topic.is_hot == -1) \
        .count()
    start = (page - 1) * per_page
    stop = start + per_page
    topic_list = db.session.query(Topic).filter(Topic.status == 1,
                                                Topic.is_hot == -1) \
        .order_by(Topic.create_time.desc()) \
        .slice(start, stop) \
        .all()
    data_list = []
    for topic in topic_list:
        info = {
            'id': topic.id,
            'title': topic.title,
            'description': topic.description,
            'img_url': topic.img_url,
            'is_hot': topic.is_hot,
            'post_count': get_post_count_by_topic_id(topic.id)
        }
        data_list.append(info)
    return count, data_list


def get_forum_topic_info_service(topic_id):
    topic = Topic.query.get(topic_id)
    if not topic:
        raise NotFound(error_code=9000, error='论坛话题不存在')
    return {
        'id': topic.id,
        'title': topic.title,
        'description': topic.description,
        'img_url': topic.img_url,
        'is_hot': topic.is_hot,
        'post_count': get_post_count_by_topic_id(topic.id),
        'share_web_url': current_app.config['SERVER_HOST_NAME'] + '/api.php?s=/forum/topicPostListView/topicId/' + str(
            topic_id)
    }


def get_post_count_by_topic_id(topic_id):
    count = db.session.query(TopicToPostRelation).filter(TopicToPostRelation.status == 1,
                                                         TopicToPostRelation.topic_id == topic_id) \
        .count()
    return count


def add_fans_count_to_recommend_users_info(user_list):
    new_user_list = []
    for user in user_list:
        info = {
            "nickname": user['nickname'],
            "path": user['path'],
            "type": user['type'],
            "uid": user['uid'],
            "fans_count": get_fans_count_by_uid(user['uid'])
        }
        new_user_list.append(info)
    return new_user_list


def get_fans_count_by_uid(uid):
    count = db.session.query(Follow).filter(Follow.follow_who == uid, Follow.type == 1).count()
    return count
