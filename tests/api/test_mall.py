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

        with self.subTest():
            # 测试当参数被修改时是否会正确提示
            wrong_sign_params = get_params+'name=33'
            url_w_sign = '/v1/mall/duiba/order' + wrong_sign_params
            r_w = self.client.get(url_w_sign)
            print(r_w.status_code, r_w.data)
            assert r_w.status_code == 400 and b'999' in r_w.data

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

    def test_create_order_duiba_not_enough_coin(self):
        """
        主要测试积分不足时候的扣分情况uid=2 只有300分
        """

        get_params = ("?uid=2&paramsTest32=32&orderNum=order-for-test-1447732196174&"
                      "credits=1000&params=15045678901&type=phonebill&ip=192.168.1.100&"
                      "sign=3680acf95d90232d406b7eb52b44eb83&timestamp=1447732196174&"
                      "waitAudit=true&actualPrice=1000&"
                      "description=%E6%89%8B%E6%9C%BA%E5%8F%B7%3A15045678901+%E5%85%85%E5%80%BC10%E5%85%83&"
                      "facePrice=1000&appKey=tLCk6CH9b3deXPbedS8TEfmLbnR&")

        user_score = db.session.query(UserCSU.score).filter_by(uid=2).first()
        url = '/v1/mall/duiba/order'+get_params
        rv = self.client.get(url)
        print(rv.data)
        assert rv.status_code == 400
        user_score_after = db.session.query(UserCSU.score).filter_by(uid=2).first()
        assert user_score_after[0] == user_score[0]
        assert user_score_after[0] == 300
        user_dynamic_credit = db.session.query(UserCSUCreditDynamic.credit_dynamic,
                                               UserCSUCreditDynamic.left_credit).first()
        assert user_dynamic_credit is None

    def test_update_order_duiba(self):
        pass

    def test_redirect_to_duiba(self):
        headers = self.get_authorized_header()
        rv = self.client.get('/v1/mall/duiba/index', headers=headers)
        http = Httper()
        r_redirect = http.get(rv.location)

        print(r_redirect.status)
        assert r_redirect.status == 200

