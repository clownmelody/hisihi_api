from herovii.models.user.user_csu_secure import UserCSUSecure
from tests.api._base import TestCase, TestUserCSUCase

__author__ = 'bliss'


class TestUserCSU(TestUserCSUCase):
    def test_password_md5(self):
        """消费用户：密码加密是否符合预期"""
        user = UserCSUSecure.query.filter_by(id=2).first()

        # 1122333 密码加密后应该为下面的数值
        should_be = '7c3307fac7459f1cd889810bdbb3e683'
        self.assertEqual(user.password, should_be)


