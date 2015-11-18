__author__ = 'bliss'

import sys
import logging
from flask_cors import CORS
from herovii import create_app
from herovii.models import db

app = create_app()
CORS(app)


if '--initdb' in sys.argv:
    sys.exit()

with app.app_context():
    db.create_all()

# 日志记录，当前测试在调试模式下，生成环境需更改为 not app.debug
if not app.debug:

    formatter = logging.Formatter(
        '[%(asctime)s %(levelname)s %(funcName)s %(filename)s:%(lineno)d]: %(message)s'
    )
    file_handler = logging.FileHandler('log.txt')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


# def logging_Mail():
#     sh =  handlers.SMTPHandler(mailhost=('localhost', 25),
#                                      fromaddr='vms@test.com',
#                                      toaddrs='test@test.com',
#                                      subject='Logged Event')

if __name__ == '__main__':
    app.run()

