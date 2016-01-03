.. _imPushService:

IM 相关操作 Push 通知定义
========

成员被移除群聊
~~~~~~~~~~~~~~~

** Push Extra Data **

.. sourcecode:: json

    {
        'type': 'removed_from_group',
        'uid': uid,
        'gid': gid
    }


用户加入群聊
~~~~~~~~~~~~~~~

** Push Extra Data **

.. sourcecode:: json

    {
        'type': 'added_to_group',
        'uid': uid,
        'gid': gid
    }


修改群信息
~~~~~~~~~~~~~~~

** Push Extra Data **

.. sourcecode:: json

    {
        'type': 'group_info_been_modified',
        'uid': uid,
        'gid': gid
    }