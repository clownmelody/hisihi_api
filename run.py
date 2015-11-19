import sys
import logging
from logging.handlers import SMTPHandler
from flask_cors import CORS
from herovii import create_app
from herovii.models import db

__author__ = 'bliss'

app = create_app()
CORS(app)


if '--initdb' in sys.argv:
    sys.exit()

with app.app_context():
    db.create_all()

# # 日志记录，当前测试在调试模式下，生成环境需更改为 not app.debug
if not app.debug:

    formatter = logging.Formatter(
        '[%(asctime)s %(levelname)s %(funcName)s %(filename)s:%(lineno)d]: %(message)s'
    )
    file_handler = logging.FileHandler('log.txt')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

    sh = SMTPHandler(
                        'smtp.qq.com', '499055803@qq.com', '499055803@qq.com', 'bugger:!!!',
                        credentials=('499055803@qq.com', 'll38966621314520'))
    sh.setFormatter(formatter)
    app.logger.addHandler(sh)


if __name__ == '__main__':
    app.run()

