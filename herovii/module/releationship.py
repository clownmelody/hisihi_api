
from flask import json
from sqlalchemy.sql.expression import text, distinct
from sqlalchemy.sql.functions import func
from herovii.models.base import SQLAlchemy
from herovii.models.base import db
from herovii.models.user.field import Field
from herovii.models.user.follow import Follow

__author__ = 'bliss'


class Relationship(object):
    def __init__(self, uid):
        self.uid = uid

    def get_follewed_users(self):
        """
        获取已经关注的用户
        :return:
        """
        users = db.session.query(Follow.who_follow).filter(Follow.follow_who == self.uid, Follow.type == 1).all()
        if users:
            follow = []
            for user in users:
                follow.append(user.who_follow)
            return follow
        else:
            return None

    def get_alumni(self, count):
        """
        获取推荐校友列表
        :param count:   数量
        :return:
        """
        followed = self.get_follewed_users()
        school = db.session.query(Field.field_data).filter(Field.uid == self.uid, Field.field_id == 36).first_or_404()
        if school:
            if followed:
                alumni = db.session.query(Field.uid).filter(Field.field_data.like('%' + school + '%'),
                                                            Field.field_id == 36,
                                                            ~Field.uid.in_(followed))\
                    .limit(count).all()
            else:
                alumni = db.session.query(Field.uid).filter(Field.field_data == school, Field.field_id == 36)\
                    .limit(count).all()
            if alumni:
                alumnis = []
                for user in alumni:
                    alumnis.append(user.uid)
                return alumnis
            else:
                return None
        else:
            return None
