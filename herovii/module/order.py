import random
import datetime
import time
from herovii.models.base import db
from herovii.models.org.teaching_course import TeachingCourse
from herovii.models.order import RebateOrder
from herovii.libs.error_code import OrgNotFound, OrderNotFindFailure
from herovii.models.org.rebate import Rebate
from herovii.models.user.user_rebate import UserRebate

__author__ = 'shaolei'


class Order(object):
    def __init__(self, uid):
        self.uid = uid

    def get_user_order_list(self, page=1, per_page=10):
        """
        获取用户订单列表
        :param page:
        :param per_page:
        :return:
        """
        start = (page - 1) * per_page
        stop = start + per_page
        order_list = db.session.query(RebateOrder).filter(RebateOrder.uid == self.uid, RebateOrder.status >= 0)\
            .order_by(RebateOrder.create_time.desc())\
            .slice(start, stop).all()
        total_count = db.session.query(RebateOrder).filter(RebateOrder.uid == self.uid, RebateOrder.status >= 0)\
            .count()
        if order_list:
            orders = []
            for order in order_list:
                order_obj = self.get_order_obj(order)
                orders.append(order_obj)
            return total_count, orders
        else:
            return 0, None

    def create_order(self, mobile, courses_id, rebate_id, num):
        """
        创建订单
        :param mobile:          手机号
        :param courses_id:      课程id
        :param rebate_id:       抵扣券id
        :param num:             数量
        :return:
        """
        oid = db.session.query(TeachingCourse.organization_id)\
            .filter(TeachingCourse.id == courses_id)\
            .first()
        if not oid:
            raise OrgNotFound()
        rebate = db.session.query(Rebate)\
            .filter(Rebate.id == rebate_id)\
            .first()
        total_price = rebate.value * num
        now = datetime.datetime.now()
        time_str = now.strftime("%Y%m%d%H%M%S")
        order_sn = time_str + str(random.randint(1000, 9999))
        with db.auto_commit():
            order = RebateOrder()
            order.price = total_price
            order.order_sn = order_sn
            order.mobile = mobile
            order.uid = self.uid
            order.courses_id = courses_id
            order.organization_id = oid.organization_id
            order.rebate_num = num
            order.rebate_id = rebate_id
            db.session.add(order)

        return self.get_order_obj(order)

    def get_order_detail(self, oid):
        """
        获取订单详情
        :param oid:     订单id
        :return:
        """
        order = db.session.query(RebateOrder).filter(RebateOrder.id == oid).first()
        if order:
            return self.get_order_obj(order)
        else:
            raise OrderNotFindFailure()

    def get_order_obj(self, order):
        courses = db.session.query(TeachingCourse.course_name, TeachingCourse.cover_pic)\
            .filter(TeachingCourse.id == order.courses_id)\
            .first()
        rebate = db.session.query(Rebate.name, Rebate.value, Rebate.rebate_value,
                                  Rebate.use_start_time, Rebate.use_end_time)\
            .filter(Rebate.id == order.rebate_id)\
            .first()
        rebate_text = str(rebate.value) + '元抵扣券抵' + str(rebate.rebate_value) + '元学费'
        user_rebate = db.session.query(UserRebate.id, UserRebate.status)\
            .filter(UserRebate.order_id == order.id, UserRebate.rebate_id == order.rebate_id)\
            .first()
        if user_rebate:
            is_use = user_rebate.status
            user_rebate_id = user_rebate.id
        else:
            is_use = 0
            user_rebate_id = 0
        cur_time = time.time()
        if cur_time > rebate.use_end_time:
            is_out_of_date = 1
        else:
            is_out_of_date = 0
        order_obj = {
                    'id': order.id,
                    'order_sn': order.order_sn,
                    'uid': order.uid,
                    'mobile': order.mobile,
                    'order_status': order.order_status,
                    'price': order.price,
                    'num': order.rebate_num,
                    'create_time': order.create_time,
                    'organization_id': order.organization_id,
                    'rebate': {
                        'id': order.rebate_id,
                        'name': rebate.name,
                        'use_start_time': rebate.use_start_time,
                        'use_end_time': rebate.use_end_time,
                        'rebate_text': rebate_text,
                        'courses_id': order.courses_id,
                        'courses_name': courses.course_name,
                        'courses_pic': courses.cover_pic,
                        'is_use': is_use,
                        'is_out_of_date': is_out_of_date,
                        'user_rebate_id': user_rebate_id
                    }
        }
        return order_obj
