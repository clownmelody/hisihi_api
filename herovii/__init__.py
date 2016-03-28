from herovii.cache import cache
from .models import db
from herovii.cache import cache

__author__ = 'bliss'


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

    config_redis = app.config['ALI_REDIS_CONFIG']
    cache.init_app(app, config=config_redis)

    register_base(app)
    register_base_blueprints(app)

    # register_app_blueprints(app)
    # register_not_found(app)
    return app

