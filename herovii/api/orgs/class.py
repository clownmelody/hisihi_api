from herovii.libs.bpbase import ApiBlueprint

__author__ = 'bliss'


api = ApiBlueprint('org')


@api.route('<int:oid>/class/<int:cid>/sign-in')
def get_class_sign_in_detail(oid, cid):
    pass


