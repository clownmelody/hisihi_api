from herovii.models.base import db

__author__ = 'bliss'


def create_org(org):
    with db.auto_commit():
        db.session.add(org)
    return org
