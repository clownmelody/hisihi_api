from herovii.libs.enums import TagType
from herovii.models.news.news_org import NewsOrg
from herovii.models.org import OrgInfo
from herovii.models.tag import Tag
from herovii.models.user.user_org import OrgAdmin

__author__ = 'bliss'

import base64
import unittest
from flask_oauthlib.utils import to_unicode, to_bytes
from herovii.models.base import db
from herovii import create_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


SQLALCHEMY_BINDS = {
    # online database
    'online': 'sqlite:///tmp/online.db',

    # app register database
    'heroapi': 'sqlite:///tmp/heroapi.db',

    # organization database
    'org': 'sqlite:///tmp/org.db',

    # consumer database
    'csu': 'sqlite:///tmp/csu.db'
}


def encode_base64(text):
    text = to_bytes(text)
    return to_unicode(base64.b64encode(text))


class TestCase(unittest.TestCase):
    def setUp(self):
        app = create_app({
            'SQLALCHEMY_BINDS': SQLALCHEMY_BINDS,
            'SECRET_KEY': 'secret',
        })
        app.testing = True

        self._ctx = app.app_context()
        self._ctx.push()

        db.init_app(app)

        db.drop_all()
        db.create_all()

        self.app = app
        self.client = app.test_client()
        self.prepare_data()

    def prepare_data(self):
        pass

    def tearDown(self):
        self._ctx.pop()

    def get_authorized_header(self, user_id=1, scope='UserCSU', expiration=7200):
        # prepare token
        token = self.generate_auth_token(user_id, 200, scope, expiration)

        return {
            'Authorization': 'basic %s' % encode_base64(str(token, 'utf-8') + ':'),
            'Content-Type': 'application/json',
        }

    def generate_auth_token(self, uid, ac_type, scope, expiration=7200):
        from flask import current_app
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'uid': uid, 'type': int(ac_type), 'scope': scope})


class TestUserCSUCase(TestCase):
    def prepare_data(self):
        prepare_csu_data()


class TestOrgCase(TestCase):
    def prepare_data(self):
        prepare_org_data()


def prepare_csu_data():
        from herovii.models.user.user_csu import UserCSU
        from herovii.models.user.user_csu_secure import UserCSUSecure

        users_csu = [
            ('leilei', 5000),
            ('zy', 300),
            ('social', 100)
        ]
        for nickname, score in users_csu:
            user = UserCSU()
            user.nickname = nickname
            user.score = score
            db.session.add(user)
        db.session.commit()

        users_secure =[
            ('1', 'aswind', 17777777777, '123123'),
            ('2', 'bliss', 18888888888, '111222333'),
            ('3', 'openid', '', '123456')
        ]

        for uid, username, mobile, password in users_secure:
            user = UserCSUSecure()
            user.id = uid
            user.username = username
            user.password = password
            user.mobile = mobile
            db.session.add(user)
        db.session.commit()


def prepare_org_data():
    users_org = [
        ('18607131949', '123123', 1),
        ('18607138888', '111222333', 2)
    ]
    for mobile, password, organization_id in users_org:
        user = OrgAdmin()
        user.mobile = mobile
        user.password = password
        user.organization_id = organization_id
        db.session.add(user)
    db.session.commit()

    news = [
        ('头条', '开业酬宾', '头条内容'),
        ('头条', '开业酬宾', '头条内容'),
        ('头条', '开业酬宾', '头条内容'),
        ('头条', '开业酬宾', '头条内容'),
        ('头条', '开业酬宾', '头条内容')
    ]
    for tag, title, content in news:
        news = NewsOrg()
        news.tag = tag
        news.title = title
        news.content = content
        db.session.add(news)
    db.session.commit()

    tags = [
        (TagType.org_advantage, '世界500强CEO授课'),
        (TagType.org_advantage, '无敌的培训学校'),
        (TagType.org_type, '设计培训'),
        (TagType.org_type, '互联网精英培训')
    ]

    for tag_type, value in tags:
        tag = Tag()
        tag.type = tag_type.value
        tag.value = value
        db.session.add(tag)
    db.session.commit()

    orgs = [
        ('北大青鸟', '培训！培训！培训万岁', '武汉市洪山区光谷新世界1602', '武汉',
         '114.421816', '30.498029', '设计培训#精英培训', 1, '0278888888', '无敌#高效', 1,
         '介绍', 'video', 'video_img', 'logo'),
        ('火星时代', '培训！培训！培训万岁', '武汉市洪山区光谷新世界1602', '北京',
         '114.421816', '30.498029', '设计培训#精英培训', 1, '0278888888', '无敌#高效', 2,
         '介绍', 'video', 'video_img', 'logo')
    ]

    for org_info in orgs:
        org = OrgInfo()
        org.name = org_info[0]
        org.slogan = org_info[1]
        org.location = org_info[2]
        org.city = org_info[3]
        org.lon = org_info[4]
        org.lat = org_info[5]
        org.type = org_info[6]
        org.audit_status = org_info[7]
        org.phone_num = org_info[8]
        org.advantage = org_info[9]
        org.uid = org_info[10]
        org.introduce = org_info[11]
        org.video = org_info[12]
        org.video_img = org_info[13]
        org.logo = org_info[14]
        db.session.add(org)
    db.session.commit()
