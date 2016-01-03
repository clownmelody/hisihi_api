# -*- coding: utf-8 -*-
import jpush as jpush
from herovii.libs.error_code import ParamException
from herovii.secure import JPUSH_APP_KEY, JPUSH_MASTER_SECRET, JPUSH_APNS_PRODUCTION

__author__ = 'yangchujie'

"""
IM 业务中的通知服务
"""


class JPushService(object):
    app_key = JPUSH_APP_KEY
    master_secret = JPUSH_MASTER_SECRET
    apns_production = JPUSH_APNS_PRODUCTION
    _jpush = jpush.JPush(app_key, master_secret)
    push = _jpush.create_push()

    @staticmethod
    def push_removed_from_group_message(reg_id=None, uid=None, gid=None):
        """
        成员被移除群聊，向所有群成员发push通知
        """
        if reg_id is None:
            raise ParamException()
        JPushService.push.audience = jpush.audience(
            jpush.registration_id(reg_id)
        )
        extras = {
            'type': 'removed_from_group',
            'uid': uid,
            'gid': gid
        }
        ios_msg = jpush.ios(alert="你被管理员移出群聊", badge="+0", sound="default", extras=extras)
        android_msg = jpush.android(alert="你被管理员移出群聊", extras=extras)
        JPushService.push.notification = jpush.notification(android=android_msg, ios=ios_msg)
        JPushService.push.options = {"time_to_live": 0, "sendno": 12345,
                                     "apns_production": JPushService.apns_production}
        JPushService.push.platform = jpush.all_
        JPushService.push.send()

    @staticmethod
    def push_added_to_group_message(reg_id=None, uid=None, gid=None):
        """
        成员被添加到群聊，向所有群成员发送push通知
        """
        if reg_id is None:
            raise ParamException()
        JPushService.push.audience = jpush.audience(
            jpush.registration_id(reg_id)
        )
        extras = {
            'type': 'added_to_group',
            'uid': uid,
            'gid': gid
        }
        ios_msg = jpush.ios(alert="XXX加入群聊", badge="+0", sound="default", extras=extras)
        android_msg = jpush.android(alert="XXX加入群聊", extras=extras)
        JPushService.push.notification = jpush.notification(android=android_msg, ios=ios_msg)
        JPushService.push.options = {"time_to_live": 0, "sendno": 12345,
                                     "apns_production": JPushService.apns_production}
        JPushService.push.platform = jpush.all_
        JPushService.push.send()

    @staticmethod
    def push_group_info_been_modified_message(reg_id=None, uid=None, gid=None):
        """
        群组基本信息被修改，向所有群成员发送push通知
        """
        if reg_id is None:
            raise ParamException()
        JPushService.push.audience = jpush.audience(
            jpush.registration_id(reg_id)
        )
        extras = {
            'type': 'group_info_been_modified',
            'uid': uid,
            'gid': gid
        }
        ios_msg = jpush.ios(alert="XXX修改了群信息", badge="+0", sound="default", extras=extras)
        android_msg = jpush.android(alert="XXX修改了群信息", extras=extras)
        JPushService.push.notification = jpush.notification(android=android_msg, ios=ios_msg)
        JPushService.push.options = {"time_to_live": 0, "sendno": 12345,
                                     "apns_production": JPushService.apns_production}
        JPushService.push.platform = jpush.all_
        JPushService.push.send()

    @staticmethod
    def push_admin_dismiss_group_message(reg_id=None, uid=None, gid=None):
        """
        群组被群管理员解散，向所有群成员发送push通知
        """
        if reg_id is None:
            raise ParamException()
        JPushService.push.audience = jpush.audience(
            jpush.registration_id(reg_id)
        )
        extras = {
            'type': 'group_been_dismissed',
            'uid': uid,
            'gid': gid
        }
        ios_msg = jpush.ios(alert="群主解散了该群", badge="+0", sound="default", extras=extras)
        android_msg = jpush.android(alert="群主解散了该群", extras=extras)
        JPushService.push.notification = jpush.notification(android=android_msg, ios=ios_msg)
        JPushService.push.options = {"time_to_live": 0, "sendno": 12345,
                                     "apns_production": JPushService.apns_production}
        JPushService.push.platform = jpush.all_
        JPushService.push.send()

