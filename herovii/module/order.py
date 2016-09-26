import random
import datetime
import time

from flask.globals import current_app

from herovii.libs.helper import make_a_coupon_code
from herovii.models.base import db
from herovii.models.org.teaching_course import TeachingCourse
from herovii.models.order import RebateOrder
from herovii.libs.error_code import OrgNotFound, OrderNotFindFailure, UserRebateNotFindFailure
from herovii.models.org.rebate import Rebate
from herovii.models.user.user_rebate import UserRebate

__author__ = 'shaolei'


class Order(object):
    def __init__(self, uid=0):
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
        total_price = int(rebate.value) * int(num)
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

    def update_order_status(self, order_sn, status):
        RebateOrder.query.filter_by(order_sn=order_sn).update({'order_status': status})
        db.session.commit()

    def check_order_status(self, order_sn):
        order = db.session.query(RebateOrder.order_status)\
            .filter(RebateOrder.order_sn == order_sn)\
            .first()
        if order.order_status > 0:
            return True
        else:
            return False

    def get_user_rebate_id(self, oid):
        user_rebate = db.session.query(UserRebate.id)\
            .filter(UserRebate.order_id == oid, UserRebate.uid == self.uid)\
            .first()
        if user_rebate:
            return user_rebate.id
        else:
            raise UserRebateNotFindFailure()

    def get_rebate_code_service(self, uid):
        coupon_code = make_a_coupon_code(uid)
        oss_url = current_app.config['WEIXIN_SERVER_HOST_NAME'] + '/scissor/index/index?rebate=' + coupon_code
        return coupon_code, oss_url

    def get_order_by_ordersn(self, order_sn):
        order = db.session.query(RebateOrder)\
            .filter(RebateOrder.order_sn == order_sn)\
            .first()
        return order

    def create_user_rebate(self, order_sn):
        user_order = self.get_order_by_ordersn(order_sn)
        promo_code, promo_code_url = self.get_rebate_code_service(user_order.uid)
        user_rebate = UserRebate()
        user_rebate.promo_code = promo_code
        user_rebate.promo_code_url = promo_code_url
        user_rebate.rebate_id = user_order.rebate_id
        user_rebate.order_id = user_order.id
        user_rebate.uid = user_order.uid
        user_rebate.teaching_course_id = user_order.courses_id
        with db.auto_commit():
            db.session.add(user_rebate)
