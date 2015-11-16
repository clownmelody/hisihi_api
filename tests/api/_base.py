__author__ = 'bliss'

import base64
import unittest
from flask_oauthlib.utils import to_unicode, to_bytes
from herovii.models.base import db
from herovii import create_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


SQLALCHEMY_BINDS = {
    'test': 'sqlite:///tmp/test1.db',

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

    def tearDown(self):
        self._ctx.pop()

    def prepare_data(self):
        from herovii.models.user.user_csu import UserCSU
        from herovii.models.user.user_csu_secure import UserCSUSecure

        users = [
            ('leilei', 5000),
            ('zy', 300),
        ]
        for nickname, score in users:
            user = UserCSU()
            user.nickname = nickname
            user.score = score
            db.session.add(user)
        db.session.commit()

        users_secure =[
            ('1', 'aswind', '123123'),
            ('2', 'bliss', '123123')
        ]

        for uid, username, password in users_secure:
            user = UserCSUSecure()
            user.id = uid
            user.username = username
            user.password = password
            db.session.add(user)
        db.session.commit()

    def get_authorized_header(self, user_id=1, scope='UserCSU',):
        # prepare token
        token = self.generate_auth_token(user_id, 200, scope)

        return {
            'Authorization': 'basic %s' % encode_base64(str(token, 'utf-8') + ':'),
            'Content-Type': 'application/json',
        }

    def generate_auth_token(self, uid, ac_type, scope, expiration=7200):
        from flask import current_app
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'uid': uid, 'type': int(ac_type), 'scope': scope})
