from sqlalchemy.orm.util import aliased
from herovii.models.base import db
from herovii.models.org.teacher_group import TeacherGroup
from herovii.models.org.teacher_group_realation import TeacherGroupRealation
from herovii.models.user.user_csu import UserCSU

__author__ = 'bliss'


def create_org_info(org):
    with db.auto_commit():
        db.session.add(org)
    return org


def get_org_teachers_by_group(oid):
    # r = TeacherGroup.query.join(
    #     TeacherGroupRealation, TeacherGroup.id == TeacherGroupRealation.teacher_group_id
    # ).all()
    # a_alias = aliased(TeacherGroupRealation)
    r1 = db.session.query(TeacherGroupRealation.uid, TeacherGroupRealation.teacher_group_id).\
        join(TeacherGroup, TeacherGroup.id == TeacherGroupRealation.teacher_group_id, aliased=True
    ).filter_by(organization_id=oid).all()
    print(r1)
    m = map(lambda x: x[0], r1)
    l = list(m)
    r2 = db.session.query(UserCSU).filter(UserCSU.uid.in_(l)).all()

    return r2

