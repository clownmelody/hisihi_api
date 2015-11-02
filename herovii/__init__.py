__author__ = 'bliss'

from .models import db


def register_base(app):
    db.init_app(app)

    # social.init_app(app)
    # auth.bind_oauth(app)
    # cache.init_app(app)
    # mail.init_app(app)
    # uploader.init_app(app)
    # bind_events()


def register_base_blueprints(app):
    from .api import init_app
    from herovii.api.authorization import auth
    init_app(app)

    app.register_blueprint(auth.bp, url_prefix='/v1/authorization')


def create_app(config=None):
    from .app import create_app
    app = create_app(config)
    register_base(app)
    register_base_blueprints(app)
    # register_app_blueprints(app)
    # register_not_found(app)
    return app

