__author__ = 'bliss'

import re

from flask import Blueprint

from herovii.handlers import account
handler_bp = Blueprint('f1', __name__)


def init_handlers(app):
    # app.wsgi_app = ApiVersionMiddleware(app.wsgi_app)
    reg_handler_bp(app)
    # reg_org_bp(app)
    # reg_auth_bp(app)


def reg_handler_bp(app):
    account.api.register(handler_bp)
    app.register_blueprint(handler_bp, url_prefix='/f1')