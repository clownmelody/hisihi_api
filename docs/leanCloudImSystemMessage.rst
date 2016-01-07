.. _leanCloudImSystemMessage:

IM 相关操作对应 LeanCloud 系统通知 Message 结构
========

成员被移除群聊
~~~~~~~~~~~~~~~

** Message Content **

.. sourcecode:: json

    {
        "message_info": "XXX 被移出群聊",
        "sys_message_type": "removed_from_group",
        "uid": uid,
        "gid": gid,
        "member_client_ids": member_client_ids
    }


用户加入群聊
~~~~~~~~~~~~~~~

** Message Content **

.. sourcecode:: json

    {
        "message_info": "XXX、XXX 加入群聊",
        "sys_message_type": "added_to_group",
        "uid": uid,
        "gid": gid,
        "member_client_ids": member_client_ids
    }


修改群信息
~~~~~~~~~~~~~~~

** Message Content **

.. sourcecode:: json

    {
        "message_info": "XXX 修改了群信息",
        "sys_message_type": "group_info_been_modified",
        "uid": uid,
        "gid": gid,
    }


群主解散群
~~~~~~~~~~~~~~~

** Message Content **

.. sourcecode:: json

     {
        "message_info": "XXX 解散了该群",
        "sys_message_type": "group_been_dismissed",
        "uid": uid,
        "gid": gid,
     }