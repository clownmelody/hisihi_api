import random
import datetime
from flask.globals import current_app
from herovii.models.base import db
from herovii.models.user.follow import Follow
from herovii.models.org.teaching_course import TeachingCourse
from herovii.models.order import RebateOrder
from herovii.libs.error_code import OrgNotFound, OrderNotFindFailure
from herovii.models.org.rebate import Rebate

__author__ = 'shaolei'


class Order(object):
    def __init__(self, uid):
        self.uid = uid

    def get_user_order_list(self):
        """
        获取用户订单列表
        :return:
        """
        order_list = db.session.query(RebateOrder).filter(RebateOrder.uid == self.uid, RebateOrder.status >= 0).all()
        if order_list:
            orders = []
            for order in order_list:
                courses = db.session.query(TeachingCourse.course_name, TeachingCourse.cover_pic)\
                    .filter(TeachingCourse.id == order.courses_id)\
                    .first()
                rebate = db.session.query(Rebate.name)\
                    .filter(Rebate.id == order.rebate_id)\
                    .first()
                order_obj = {
                    'id': order.id,
                    'order_sn': order.order_sn,
                    'uid': order.uid,
                    'mobile': order.mobile,
                    'pay_status': order.pay_status,
                    'order_status': order.order_status,
                    'price': order.price,
                    'courses_id': order.courses_id,
                    'courses_name': courses.course_name,
                    'courses_pic': courses.cover_pic,
                    'rebate_id': order.rebate_id,
                    'rebate_name': rebate.name,
                    'num': order.rebate_num,
                    'create_time': order.create_time
                }
                orders.append(order_obj)
            return orders
        else:
            return None

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
        per_price = db.session.query(Rebate.value)\
            .filter(Rebate.id == rebate_id)\
            .first()
        total_price = per_price.value * num
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
        return order

    def get_order_detail(self, oid):
        """
        获取订单详情
        :param oid:     订单id
        :return:
        """
        order = db.session.query(RebateOrder).filter(RebateOrder.id == oid).first()
        if order:
            courses = db.session.query(TeachingCourse.course_name, TeachingCourse.cover_pic)\
                .filter(TeachingCourse.id == order.courses_id)\
                .first()
            rebate = db.session.query(Rebate.name, Rebate.value, Rebate.rebate_value,
                                      Rebate.use_start_time, Rebate.use_end_time)\
                .filter(Rebate.id == order.rebate_id)\
                .first()
            rebate_text = str(rebate.value) + '元抵扣券抵' + str(rebate.rebate_value) + '元学费'
            order_obj = {
                    'id': order.id,
                    'order_sn': order.order_sn,
                    'uid': order.uid,
                    'mobile': order.mobile,
                    'pay_status': order.pay_status,
                    'order_status': order.order_status,
                    'price': order.price,
                    'courses_id': order.courses_id,
                    'courses_name': courses.course_name,
                    'courses_pic': courses.cover_pic,
                    'rebate_id': order.rebate_id,
                    'rebate_name': rebate.name,
                    'num': order.rebate_num,
                    'create_time': order.create_time,
                    'use_start_time': rebate.use_start_time,
                    'use_end_time': rebate.use_end_time,
                    'rebate_text': rebate_text
            }
            return order_obj
        else:
            raise OrderNotFindFailure()
