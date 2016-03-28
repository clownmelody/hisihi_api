from herovii.cache import cache

__author__ = 'bliss'

from .models import db
from herovii.cache import cache


def register_base(app):
    db.init_app(app)

    # social.init_app(app)
    # auth.bind_oauth(app)
    # cache.init_app(app)
    # mail.init_app(app)
    # uploader.init_app(app)
    # bind_events()


def register_base_blueprints(app):
    from .api import init_api
    # from .handlers import init_handlers
    init_api(app)
    # init_handlers(app)


def create_app(config=None):
    from .app import create_app
    app = create_app(config)

    # config = {
    # 'CACHE_TYPE': 'redis',
    # 'CACHE_KEY_PREFIX': 'herovii_dev',
    # 'CACHE_REDIS_HOST': '0144e112abe149ed.m.cnqda.kvstore.aliyuncs.com',
    # 'CACHE_REDIS_PORT': 6379,
    # 'CACHE_REDIS_PASSWORD': '027Xunniutech',
    # 'CACHE_REDIS_DB': 6
    # }

    config = {
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'herovii_dev',
    'CACHE_REDIS_HOST': '115.29.32.161',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_PASSWORD': '027Xunniutech',
    'CACHE_REDIS_DB': 6
    }

    cache.init_app(app, config=config)

    register_base(app)
    register_base_blueprints(app)

    # register_app_blueprints(app)
    # register_not_found(app)
    return app

