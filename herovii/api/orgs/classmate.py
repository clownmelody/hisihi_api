
from herovii.libs.bpbase import ApiBlueprint, auth

__author__ = 'bliss'


api = ApiBlueprint('org')


@api.route('/<int:oid>/class/<int:cid>/sign-in/<date>/detail')
def get_class_sign_in_detail(oid, cid, date):
    """获取签到情况，按班级分类
       分页参数：page， per_page (可选)， 参见org/stats下的sin_in_count_stats 处理方式
       oid : 机构id号
       date: 日期 2015-12-10
       cid: 班级号
       请完成接口并测试后在方法上添加@auth.login_required
       最后在docs/classmate 里编写文档
    """
    # Todo: @杨楚杰
    pass