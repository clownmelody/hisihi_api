# -*- coding: utf-8 -*-
import json
from flask import current_app
from herovii.libs.util import get_oss_pic_path_by_pic_id
from herovii.models.InformationFlow.document import Document
from herovii.models.InformationFlow.document_acticle import DocumentArticle
from herovii.models.InformationFlow.favorite import Favorite

from herovii.models.InformationFlow.information_flow_banner import InformationFlowBanner
from herovii.models.InformationFlow.information_flow_content import InformationFlowContent
from herovii.models.InformationFlow.support import Support
from herovii.models.base import db

__author__ = 'yangchujie'


# 头条是否被用户点赞
def is_article_support(uid, article_id):
    is_support = db.session.query(Support).filter(Support.row == article_id,
                                                  Support.appname == 'Article',
                                                  Support.uid == uid) \
        .count()
    if is_support:
        return True
    else:
        return False


# 头条是否被用户收藏
def is_article_favorite(uid, article_id):
    is_favorite = db.session.query(Favorite).filter(Favorite.row == article_id,
                                                    Favorite.appname == 'Article',
                                                    Favorite.uid == uid) \
        .count()
    if is_favorite:
        return True
    else:
        return False


# 头条的点赞数量
def get_article_support_count(article_id):
    real_count = db.session.query(Support).filter(Support.row == article_id,
                                                  Support.appname == 'Article') \
        .count()
    article = db.session.query(DocumentArticle).filter(DocumentArticle.id == article_id).first()
    if article:
        return real_count + int(article.fake_support_count)
    else:
        return real_count
