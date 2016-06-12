# -*- coding: utf-8 -*-
from herovii import db
from herovii.models.forum.TopicToPostRelation import TopicToPostRelation
from herovii.models.forum.topic import Topic

__author__ = 'yangchujie'


def get_forum_hot_topic_list_service():
    count = db.session.query(Topic).filter(Topic.status == 1,
                                           Topic.is_hot == 1) \
        .count()
    topic_list = db.session.query(Topic).filter(Topic.status == 1,
                                                Topic.is_hot == 1) \
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
        .order(Topic.create_time.desc()) \
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


def get_post_count_by_topic_id(topic_id):
    count = db.session.query(TopicToPostRelation).filter(TopicToPostRelation.status == 1,
                                                         TopicToPostRelation.topic_id == topic_id) \
        .count()
    return count
