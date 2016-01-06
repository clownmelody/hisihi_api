from herovii.libs.bpbase import ApiBlueprint

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/<int:oid>/message/course_schedule/broadcast')
def broadcast_course_schedule(oid):
    pass