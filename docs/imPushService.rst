.. _imPushService:

IM 相关操作 Push 通知定义
========

成员被移除群聊
~~~~~~~~~~~~~~~

** Push Extra Data **

.. sourcecode:: json

    {
        "_lctype": -1,
        "_lctext": "XXX 被移出群聊",
        "_lcattrs": {
            "message_info": "XXX 被移出群聊",
            "sys_message_type": "removed_from_group",
            "uid": "c001",
            "gid": 2,
            "member_client_ids": ["c001", "c002"]
        }
    }


用户加入群聊
~~~~~~~~~~~~~~~

** Push Extra Data **

.. sourcecode:: json

    {
        "_lctype": 1,
        "_lctext": "XXX、XXX 加入群聊",
        "_lcattrs": {
            "message_info": "XXX、XXX 加入群聊",
            "sys_message_type": "added_to_group",
            "uid": "c001",
            "gid": 2,
            "member_client_ids": ["c001", "c002"]
        }
    }


修改群信息
~~~~~~~~~~~~~~~

** Push Extra Data **

.. sourcecode:: json

    {
        "_lctype": 1,
        "_lctext": "XXX 修改了群信息",
        "_lcattrs": {
            "message_info": "XXX 修改了群信息",
            "sys_message_type": "group_info_been_modified",
            "uid": "c001",
            "gid": 2,
        }
    }


群主解散群
~~~~~~~~~~~~~~~

** Push Extra Data **

.. sourcecode:: json

    {
        "_lctype": 1,
        "_lctext": "XXX 解散了该群",
        "_lcattrs": {
            "message_info": "XXX 解散了该群",
            "sys_message_type": "group_been_dismissed",
            "uid": "c001",
            "gid": 2,
        }
    }


用户加群申请
~~~~~~~~~~~~~~~

** Push Extra Data **

.. sourcecode:: json

    {
        "_lctype": 1,
        "_lctext": "XXX 申请加入该群",
        "_lcattrs": {
            "message_info": "XXX 申请加入该群",
            "sys_message_type": "user_join_group_apply",
            "uid": "c001",
            "gid": 2,
        }
    }