from herovii.libs.bpbase import ApiBlueprint

__author__ = 'bliss'


api = ApiBlueprint('org')


@api.route('/<int:oid>/sign-in/count/status')
def get_sign_in_count_stats(oid):
    pass


@api.route('/<int:oid>/class/sign-in/count/status')
def get_list_class_sign_in_count_status(oid):
    pass
