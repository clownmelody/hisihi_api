__author__ = 'bliss'


from ._base import TestCase
from herovii.libs.httper import Httper
from herovii.models.base import db
from herovii.models.user.user_csu_credit_dynamic import UserCSUCreditDynamic
from herovii.models.user.user_csu import UserCSU


class TestMall(TestCase):

    def test_create_order_duiba(self):
        """
        主要测试积分的扣除是否正常
        """

        get_params = ("?uid=1&orderNum=order-for-test-1447670790415&"
                      "credits=1000&params=15045678901&type=phonebill&"
                      "paramsTest10=10&ip=192.168.1.100&sign=4ae02d3ac2e007f877b8912361445780&"
                      "timestamp=1447670790415&waitAudit=true&actualPrice=1000&"
                      "description=%E6%89%8B%E6%9C%BA%E5%8F%B7%3A15045678901+%E5%85%85%E5%80%BC10%E5%85%83&"
                      "facePrice=1000&appKey=tLCk6CH9b3deXPbedS8TEfmLbnR&")
        user_score = db.session.query(UserCSU.score).filter_by(uid=1).first()
        url = '/v1/mall/duiba/order'+get_params
        rv = self.client.get(url)
        assert rv.status_code == 200
        user_score_after = db.session.query(UserCSU.score).filter_by(uid=1).first()
        assert user_score_after[0] == user_score[0] - 1000
        user_dynamic_credit = db.session.query(UserCSUCreditDynamic.credit_dynamic,
                                               UserCSUCreditDynamic.left_credit).first()
        dynamic_credit = user_dynamic_credit[0]
        left_credit = user_dynamic_credit[1]
        assert dynamic_credit == -1000
        assert left_credit == user_score_after[0]

    def test_update_order_duiba(self):
        pass

    def test_redirect_to_duiba(self):
        headers = self.get_authorized_header()
        rv = self.client.get('/v1/mall/duiba/index', headers=headers)
        http = Httper()
        r_redirect = http.get(rv.location)

        print(r_redirect.status)
        assert r_redirect.status == 200

