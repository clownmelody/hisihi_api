import random

from herovii.libs.helper import get_full_oss_url
from herovii.models.base import db
from herovii.models.user.avatar import Avatar
from herovii.models.user.field import Field
from herovii.models.user.follow import Follow
from herovii.models.user.user_csu import UserCSU

__author__ = 'bliss'


class Relationship(object):
    def __init__(self, uid):
        self.uid = uid

    def get_followed_users(self):
        """
        获取已经关注的用户uid列表
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

    def get_alumni(self, count, recommend_id=None):
        """
        获取校友推荐id列表
        :param count: 数量
        :param recommend_id: 上次推荐的id
        :return:
        """
        followed = self.get_followed_users()
        if recommend_id:
            followed.extend(recommend_id)
            followed = list(set(followed))
        school = db.session.query(Field.field_data).filter(Field.uid == self.uid, Field.field_id == 36).first()
        if school:
            if followed:
                followed.append(self.uid)
                alumni = db.session.query(Field.uid).filter(Field.field_data.like('%' + school[0] + '%'),
                                                            Field.field_id == 36,
                                                            ~Field.uid.in_(followed))\
                    .all()
            else:
                alumni = db.session.query(Field.uid).filter(Field.field_data == school, Field.field_id == 36)\
                    .all()
            if alumni:
                alumnis = []
                if len(alumni) <= count:
                    for user in alumni:
                        alumnis.append(user.uid)
                    return alumnis
                else:
                    random.shuffle(alumni)
                    for i in range(0, count):
                        alumnis.append(alumni[i].uid)
                    return alumnis
            else:
                return None
        else:
            return None

    def get_recommend_users(self, count=None, recommend_id=None):
        """
        获取推荐的人id列表
        :param count: 数量
        :param recommend_id: 上次推荐的id
        :return:
        """
        followed = self.get_followed_users()
        if recommend_id:
            followed.extend(recommend_id)
            followed = list(set(followed))
        if followed:
            followed.append(self.uid)
            if count:
                alumni = db.session.query(UserCSU.uid).filter(UserCSU.status == 4,
                                                              ~UserCSU.uid.in_(followed))\
                    .limit(count).all()
            else:
                alumni = db.session.query(UserCSU.uid).filter(UserCSU.status == 4,
                                                              ~UserCSU.uid.in_(followed))\
                    .all()
        else:
            if count:
                alumni = db.session.query(UserCSU.uid).filter(UserCSU.status == 4)\
                    .limit(count).all()
            else:
                alumni = db.session.query(UserCSU.uid).filter(UserCSU.status == 4)\
                    .all()
        if alumni:
            alumnis = []
            for user in alumni:
                alumnis.append(user.uid)
            return alumnis
        else:
            return None

    def merge_recommend_users(self):
        """
        合并推荐的人
        :return:
        """
        id_list = []
        user_list = []
        a_users = self.get_alumni(3)
        if a_users and len(a_users) > 0:
            id_list.extend(a_users)
            a_list = db.session.query(UserCSU.uid, UserCSU.nickname, Avatar.path)\
                .join(Avatar, UserCSU.uid == Avatar.uid)\
                .filter(UserCSU.uid.in_(a_users), Avatar.is_temp == 0)\
                .all()
            if len(a_list) > 0:
                for user in a_list:
                    path = user.path
                    if not user.path or user.path.strip() is '':
                        path = None
                    if not user.path.strip().startswith('http://'):
                         path = get_full_oss_url(user.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
                    u = {
                        'uid': user.uid,
                        'nickname': user.nickname,
                        'path': path,
                        'type': 'alumni'
                    }
                    user_list.append(u)
        r_users = self.get_recommend_users()
        if r_users and len(r_users) > 0:
            id_list.extend(r_users)
            r_list = db.session.query(UserCSU.uid, UserCSU.nickname, Avatar.path)\
                .join(Avatar, UserCSU.uid == Avatar.uid)\
                .filter(UserCSU.uid.in_(r_users), UserCSU.status == 4, Avatar.is_temp == 0)\
                .all()
            if len(r_list) > 0:
                for user in r_list:
                    path = user.path
                    if not user.path or user.path.strip() is '':
                        path = None
                    if not user.path.strip().startswith('http://'):
                        path = get_full_oss_url(user.path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
                    u = {
                        'uid': user.uid,
                        'nickname': user.nickname,
                        'path': path,
                        'type': 'recommend'
                    }
                    user_list.append(u)
        if user_list and len(user_list) > 0:
            data_list = {
                'count': len(user_list),
                'users': user_list,
                'recommend_id':  ','.join(str(i) for i in id_list)
            }
        else:
            data_list = {
                'count': 0,
                'users': None,
                'recommend_id': None
            }
        return data_list

    def return_another_recommend_user(self, recommend_type=None, recommend_id=None):
        """
        返回一个新的推荐用户
        :param recommend_type:
        :param recommend_id:
        :return:
        """
        if recommend_type is None:
            recommend_type = 'recommend'
        if recommend_id is None:
            recommend_id = [self.uid]
        if recommend_type == 'recommend':
            uid = self.get_recommend_users(1, recommend_id)
        else:
            uid = self.get_alumni(1, recommend_id)
        if uid:
            user = db.session.query(UserCSU.uid, UserCSU.nickname, Avatar.path)\
                        .join(Avatar, UserCSU.uid == Avatar.uid)\
                        .filter(UserCSU.uid == uid, Avatar.is_temp == 0)\
                        .all()
            if user:
                path = user[0].path
                if not user[0].path or user[0].path.strip() is '':
                    path = None
                if not user[0].path.strip().startswith('http://'):
                    path = get_full_oss_url(user[0].path, bucket_config='ALI_OSS_AVATAR_BUCKET_NAME')
                u = {
                        'uid': user[0].uid,
                        'nickname': user[0].nickname,
                        'path': path,
                        'type': recommend_type
                    }
                return u
            else:
                return None
        else:
            return None

    def follow_user(self, follow_uid):
        """
        关注用户
        :param follow_uid: 关注人uid
        :return:
        """
        followed = db.session.query(Follow)\
            .filter(Follow.who_follow == self.uid, Follow.follow_who == follow_uid, Follow.type == 1)\
            .all()
        if followed:
            return False
        with db.auto_commit():
            follow = Follow()
            follow.follow_who = follow_uid
            follow.who_follow = self.uid
            db.session.add(follow)
        return follow
