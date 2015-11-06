__author__ = 'bliss'

from datetime import datetime
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%SZ')
        return JSONEncoder.default(self, o)
#


class Flask(_Flask):
    json_encoder = JSONEncoder


def create_app(config=None):
    app = Flask(__name__)

    #: load default configuration
    app.config.from_object('herovii.settings')
    app.config.from_object('herovii.secure')

    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    return app
