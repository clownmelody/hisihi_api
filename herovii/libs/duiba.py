__author__ = 'bliss'

import hashlib, datetime
from flask import current_app
from herovii.models.mall.order_duiba import OrderDuiBa
from herovii.models.user.user_csu import UserCSU
from herovii.models.user.user_csu_credit_dynamic import UserCSUCreditDynamic
from herovii.models.base import db
from herovii.libs.helper import dict_to_url_param, make_an_bizid


class DuiBa(object):

    DUIBA_URL = r'http://www.duiba.com.cn/autoLogin/autologin'

    def sorted_values(self, params_list):
        """传入dict，返回按照参数名称升序排列的参数值字符串
        :param params_list: dict类型的数据
        :return:
        """
        sorted_items = sorted(params_list.items(), key=lambda d: d[0])

        # 将list的key去掉，只保留value, 并将所有value都转型成字符串
        m = map(lambda x: str(x[1]), sorted_items)

        # 将元组转换为字符串并输出
        ascending_values = ''.join(m)
        return ascending_values

    def md5_check(self, params_list, sign):
        """验证params_list中的数据是否符合MD5加密
        :param params_list: dict类型
        :param sign: MD5签名
        :return:
        """

        # 兑吧的字符串需要按照字母的升序排列
        # 注意：是按照字典中key的字母升序来排列

        md5 = self.create_sign(params_list)
        if md5 == sign:
            return True
        else:
            return False

    def create_sign(self, params_list):
        ascending_values = self.sorted_values(params_list)
        m = hashlib.md5()
        m.update(ascending_values.encode('utf-8'))
        sign = m.hexdigest()
        return sign

    def create_order(self, params_list):
        """ 创建有兑吧生成的订单（记录兑吧的订单数据）并扣除分数
        :param params_list: 一组dict类型的数据
        :return:
        """
        # 将兑吧的App_Secret加入到校验字符串中
        params_list['appSecret'] = current_app.config['DUIBA_APP_SECRET']
        sign = params_list['sign']

        # 去除字典中的sign，因为sign本身不属于被签名部分
        del(params_list['sign'])
        valid = self.md5_check(params_list, sign)

        # 校验完后再加入，并存入到数据库中
        params_list['sign'] = sign
        params_list['bizId'] = make_an_bizid()
        self.__adapter(params_list)
        if valid:

            # 先扣除积分再生成订单，如果某一步操作错误，需要回滚数据
            with db.auto_commit():
                success, left_credit = self.__deduct_credit(int(params_list['uid']),
                                                            int(params_list['credits']))
                if success:
                    self.__add_one_order(params_list)
                    # 注意下面的params_list['credits']需要取负数表示扣除
                    self.__add_a_credit_dynamic(params_list['uid'], -int(params_list['credits']),
                                                params_list['description'], '兑吧', left_credit)
                return success, left_credit, params_list['bizId']
        else:
            return None

    def confirm_order(self, params_list):
        """确认订单状态，反馈兑换结果"""
        # 将兑吧的App_Secret加入到校验字符串中
        params_list['appSecret'] = current_app.config['DUIBA_APP_SECRET']
        sign = params_list['sign']

        # 去除字典中的sign，因为sign本身不属于被签名部分
        del(params_list['sign'])
        valid = self.md5_check(params_list, sign)
        if valid:
            return self.__update_order(
                params_list['success'], params_list['appKey'],
                params_list['orderNum'], params_list['errorMessage'],
                params_list['timestamp'])
        else:
            return "who distort my data?"

    def create_login_url(self, uid, left_credits):
        """生成免登陆Url"""
        url_params = {
            'uid': uid,
            'appKey': current_app.config['DUIBA_APP_KEY'],

            # duiba requires timestamp must be millisecond unit, so multiply 1000
            'timestamp': int(datetime.datetime.now().timestamp()) * 1000,
            'credits': left_credits,
            'appSecret': current_app.config['DUIBA_APP_SECRET']
        }
        sign = self.create_sign(url_params)
        url_params['sign'] = sign
        del(url_params['appSecret'])
        get_params = dict_to_url_param(url_params)
        return DuiBa.DUIBA_URL+get_params

    def __add_a_credit_dynamic(self, uid, credit, reason, party,
                               left_credit):
        """向数据库写入一条积分动态"""
        dynamic = UserCSUCreditDynamic()
        dynamic.uid = uid
        dynamic.credit_dynamic = credit
        dynamic.left_credit = left_credit
        dynamic.reason = reason
        dynamic.party = party
        db.session.add(dynamic)

    def __update_order(self, success, app_key, order_num,
                       error_msg, timestamp):
        """更新订单状态"""
        order = OrderDuiBa.query.\
            filter_by(appKey=app_key, orderNum=order_num).first()
        if order is None:
            return "strange order_number which we don't recognize"
        # we must confirm the order's status never be changed
        if order.success == 0:
            if success == 'true':
                # if success, mark the order status success
                order.success = 1
                order.confirm_timestamp = timestamp
                db.session.commit()
                return 'ok'
            if success == 'false':
                # if failed, mark the order status failed
                # the whole process, must be in a transaction
                with db.auto_commit():
                    order.success = -1
                    order.error_message = error_msg
                    order.confirm_timestamp = timestamp
                    left_credit = self.__rollback_credit(order.uid, order.credits)
                    self.__add_a_credit_dynamic(order.uid, order.credits,
                                                '兑吧出错，回滚积分', 'system', left_credit)
                return 'ok'
            return "fuck, no 'true' no 'false', what's this?"
        # if order.success != 0 means this order has been updated,
        # should never be updated again
        return "i have been updated the order's status, leave me in peace"

    def __rollback_credit(self, uid, credit):
        """如果兑吧未能成功兑换，回滚用户积分"""
        user_csu = UserCSU.query.filter_by(uid=uid).first()
        user_csu.score += credit
        return user_csu.score

    def __deduct_credit(self, uid, reduced_credit):
        """扣除分数, 如果分数不够则不会扣除"""
        user_csu = UserCSU.query.filter(UserCSU.uid == uid).first()
        left_score = user_csu.score - reduced_credit
        if left_score >= 0:

            # UserCSU.query.filter(UserCSU.uid == uid).update({'score': UserCSU.score - credit})
            user_csu.score = left_score
            return True, left_score
        else:
            return False, user_csu.score

    def __add_one_order(self, params_list):
        """添加一条订单"""
        order = OrderDuiBa(**params_list)
        db.session.add(order)

    def __adapter(self, params_list):
        """
        由兑吧传入的boolean类型值为 ‘true’ 或者‘false’，需要变更为Python类型
        """
        if params_list['waitAudit'] == 'false':
            params_list['waitAudit'] = False
        else:
            params_list['waitAudit'] = True





