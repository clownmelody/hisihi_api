from herovii.libs.bpbase import ApiBlueprint

__author__ = 'bliss'

api = ApiBlueprint('org')


@api.route('/<int:oid>/enroll/blzs')
def list_blzs(oid):
    # TODO: remember return user's tel and aver
    pass


@api.route('/<int:oid>/enroll/blzs/<int:blz_id>')
def view_blz(oid, blz_id):
    pass

