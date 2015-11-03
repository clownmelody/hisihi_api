__author__ = 'bliss'

import sys
from flask_cors import CORS
from herovii import create_app
from herovii.models import db

app = create_app({'DEBUG': True})
CORS(app)


def create_database():
    # import fixtures
    with app.app_context():
        db.drop_all()
        db.create_all()
        # fixtures.run()

if '--initdb' in sys.argv:
    create_database()
    sys.exit()

with app.app_context():
    db.create_all()

# 日志记录，当前测试在调试模式下，生成环境需更改为 not app.debug
if app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler('log.txt')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run()

