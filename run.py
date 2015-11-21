import sys
import logging
from logging.handlers import SMTPHandler
from flask_cors import CORS
from herovii import create_app
from herovii.libs.error_code import ParamException, NotFound, ServerError
from herovii.models import db
from flask.ext.sqlalchemy import get_debug_queries
from herovii.secure import DATABASE_QUERY_TIMEOUT


__author__ = 'bliss'

app = create_app()
CORS(app)


if '--initdb' in sys.argv:
    sys.exit()

if app.config['CHECK_DB']:
    with app.app_context():
        db.create_all()

# # 日志记录，当前测试在调试模式下，生成环境需更改为 not app.debug
if not app.debug:

    formatter = logging.Formatter(
        '[%(asctime)s %(levelname)s %(funcName)s %(filename)s:%(lineno)d]: %(message)s'
    )
    file_handler = logging.FileHandler(app.config['LOG_FILE'])
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

    if app.config['SEND_LOG_EMAIL']:
        sh = SMTPHandler(
                            ('smtp.exmail.qq.com', 25), 'leilei@hisihi.com', '499055803@qq.com', 'bugger:!!!',
                            credentials=('leilei@hisihi.com', 'Abc123321'))
        sh.setFormatter(formatter)
        app.logger.addHandler(sh)


@app.after_request
def after_request(response):
    """数据库性能测试"""
    for query in get_debug_queries():
        print(query.duration)
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
                               (query.statement, query.parameters, query.duration, query.context))
    return response


@app.errorhandler(404)
def page_not_found(e):
    return NotFound()


@app.errorhandler(500)
def page_not_found(e):
    return ServerError()

if __name__ == '__main__':
    app.run()

