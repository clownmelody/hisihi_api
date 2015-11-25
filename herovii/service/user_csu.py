from herovii.models.base import db
from herovii.models.user.id_realeation import IdRelation

__author__ = 'bliss'


def db_change_indentity(uid, identity):
    identity_realation = IdRelation.query.filter_by(uid=uid).first_or_404()
    identity_realation.group_id = identity
    db.session.commit()
    return identity_realation
