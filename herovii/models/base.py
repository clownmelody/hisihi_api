__author__ = 'bliss'

import datetime
from contextlib import contextmanager
from sqlalchemy import Column, Integer
from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

__all__ = ['db', 'CACHE_TIMES', 'Base', 'JSON', 'ARRAY']


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.exception('%r' % e)
            if throw:
                raise e

db = SQLAlchemy(session_options={
    'expire_on_commit': False,
    'autoflush': False,
})


class BaseMixin(object):
    def __getitem__(self, key):
        return getattr(self, key)


class  Base(db.Model, BaseMixin):
    __abstract__ = True
    create_time = Column(Integer, default=int(datetime.datetime.now().timestamp()))

