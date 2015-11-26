from sqlalchemy.orm.util import aliased
from sqlalchemy.sql.expression import select
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

    collection = db.session.query(TeacherGroupRealation.uid, TeacherGroupRealation.teacher_group_id,
                                  TeacherGroup.title).\
        join(TeacherGroup, TeacherGroup.id == TeacherGroupRealation.teacher_group_id).filter_by(organization_id=oid).all()

    m = map(lambda x: x[0], collection)
    l = list(m)
    teachers = db.session.query(UserCSU).filter(UserCSU.uid.in_(l)).all()

    return dto_teachers_group(oid, collection, teachers)


def dto_teachers_group(oid, l, teachers):
    # groups = []
    group_keys = {}
    for t in teachers:
        for uid, group_id, title in l:
            if uid == t.uid:
                if group_keys.get(group_id):
                    group_keys[group_id]['teachers'].append(t)
                    # group_keys.append(group_id)

                else:
                    group = {
                        'group_id': group_id,
                        'group_title': title,
                        'teachers': [t]
                    }
                    group_keys[group_id] = group

    groups = tuple(group_keys.values())
            # if uid == t.uid:
            #     combine = {
            #         'group_id': group_id,
            #         'group_title': title,
            #         'teacher': t
            #     }
            #     groups.append(combine)

    return {
        'org_id': oid,
        'groups': groups
    }

