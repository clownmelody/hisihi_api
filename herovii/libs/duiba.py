__author__ = 'bliss'

import hashlib
from flask import current_app
from herovii.models.mall.order_duiba import OrderDuiBa
from herovii.models.user.user_csu import UserCSU
from herovii.models.base import db


class DuiBa(object):
    def sorted_values(self, params_list):
        """传入dict，返回按照参数名称升序排列的参数值字符串
        :param params_list: dict类型的数据
        :return:
        """
        sorted_items = sorted(params_list.items(), key=lambda d: d[0])

        # 将list的key去掉，只保留value
        m = map(lambda x: x[1], sorted_items)

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
        ascending_values = self.sorted_values(params_list)
        m = hashlib.md5()
        m.update(ascending_values.encode('utf-8'))
        md5 = m.hexdigest()
        if md5 == sign:
            return True
        else:
            return False

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
        self.__adapter(params_list)
        if valid:

            # 先扣除积分再生成订单，如果某一步操作错误，需要回滚数据
            with db.auto_commit():
                success, left_score = self.__deduct_credit(int(params_list['uid']),
                                                           int(params_list['credits']))
                if success:
                    self.__add_one_order(params_list)
                return success, left_score, params_list['orderNum']
        else:
            return None

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




