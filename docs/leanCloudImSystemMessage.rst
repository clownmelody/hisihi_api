.. _leanCloudImSystemMessage:

IM 相关操作对应 LeanCloud 系统通知 Message 结构
========

成员被移除群聊
~~~~~~~~~~~~~~~

** Message Content **

.. sourcecode:: json

    {
        "_lctype": 1,
        "_lctext": "XXX 被移出群聊",
        "_lcattrs": {
            "message_info": "XXX 被移出群聊",
            "sys_message_type": "removed_from_group",
            "uid": uid,
            "gid": gid,
            "type": "group",
            "conversation_id": "sf132fwedqfe",
            "member_client_ids": member_client_ids
        }
    }


用户加入群聊
~~~~~~~~~~~~~~~

** Message Content **

.. sourcecode:: json

    {
        "_lctype": 1,
        "_lctext": "XXX、XXX 加入群聊",
        "_lcattrs": {
            "message_info": "XXX、XXX 加入群聊",
            "sys_message_type": "added_to_group",
            "uid": uid,
            "gid": gid,
            "type": "group",
            "conversation_id": "sf132fwedqfe"
            "member_client_ids": member_client_ids
        }
    }


修改群信息
~~~~~~~~~~~~~~~

** Message Content **

.. sourcecode:: json

    {
        "_lctype": 1,
        "_lctext": "XXX 修改了群信息",
        "_lcattrs": {
            "message_info": "XXX 修改了群信息",
            "sys_message_type": "group_info_been_modified",
            "uid": uid,
            "gid": gid,
            "type": "group",
            "conversation_id": "sf132fwedqfe"
        }
    }


群主解散群
~~~~~~~~~~~~~~~

** Message Content **

.. sourcecode:: json

     {
        "_lctype": 1,
        "_lctext": "XXX 修改了群信息",
        "_lcattrs": {
            "message_info": "XXX 解散了该群",
            "sys_message_type": "group_been_dismissed",
            "uid": uid,
            "gid": gid,
            "type": "group",
            "conversation_id": "sf132fwedqfe"
        }
     }


用户申请加入群
~~~~~~~~~~~~~~~

** Message Content **

.. sourcecode:: json

     {
        "_lctype": 1,
        "_lctext": "XXX 修改了群信息",
        "_lcattrs": {
            "message_info": "XXX 申请加入该群",
            "sys_message_type": "user_join_group_apply",
            "uid": uid,
            "gid": gid,
            "type": "group",
            "conversation_id": "sf132fwedqfe"
        }
    }