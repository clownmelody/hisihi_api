__author__ = 'bliss'

import hashlib
from flask import current_app
from herovii.models.mall.order_duiba import OrderDuiBa
from herovii.models.base import db


class DuiBa(object):
    def sorted_values(self, params_list):
        """
        传入Url的参数字典，返回按照参数名称升序排列的参数值字符串
        :param params_list: url get参数的参数字典
        :return:
        """
        sorted_items = sorted(params_list.items(), key=lambda d: d[0])

        # 将list的key去掉，只保留value
        m = map(lambda x: x[1], sorted_items)
        ascending_values = ''.join(m)

        return ascending_values

    def md5_check(self, params_list, sign):
        ascending_values = self.sorted_values(params_list)
        m = hashlib.md5()
        m.update(ascending_values.encode('utf-8'))
        md5 = m.hexdigest()
        if md5 == sign:
            return True
        else:
            return False

    def create_order(self, params_list):

        # 将兑吧的App_Secret加入到校验字符串中
        params_list['appSecret'] = current_app.config['DUIBA_APP_SECRET']
        sign = params_list['sign']

        # 去除字典中的sign，因为sign本身不属于被签名部分
        del(params_list['sign'])

        valid = self.md5_check(params_list, sign)

        # 校验完后再加入，并存入到数据库中
        params_list['sign'] = sign
        self.__adapter(params_list)
        # m = map(self.__adapter, params_list.items())
        # l = dict(m)
        if valid:
            order = OrderDuiBa(**params_list)
            with db.auto_commit():
                db.session.add(order)
            return order
        else:
            return None

    def deduct_credit(self, uid, credit):
        pass

    def __adapter(self, params_list):
        """
        由兑吧传入的boolean类型值为 ‘true’ 或者‘false’，需要变更为Python类型
        :param dicts:
        :return:
        """
        if params_list['waitAudit'] == 'false':
            params_list['waitAudit'] = False
        else:
            params_list['waitAudit'] = True




