.. _im:

IM
==========

leancloud client-id 约定
~~~~~~~~~~~~~~~~~~~~
约定任意用户的client-id 命名规则为:

用户（包括老师、学生等）使用 'c' 作为前缀并附加其uid号，如，c565

机构（特指机构管理员）实用 'o' 作为前缀并附件其id号，如，o3

获取登陆操作签名
~~~~~~~~~~~~~~~
**URL**::

    GET     /im/signature/login/<string:app_id>/<string:client_id>

**Parameters**:

* app_id: 应用的 id
* client_id: 登录时使用的 clientId

**Response** `200` ::

    {
      "timestamp":"1450166986.392033",
      "signature":"f389a31dfa75212d7dbe196f987a973345b40500",
      "nonce":"cdXsciFc",
      "app_id":"2",
      "client_id":"3"
    }

-- end


获取开启会话操作签名
~~~~~~~~~~~~~~~
**URL**::

    GET     /im/signature/conversation/<string:app_id>/<string:client_id>/<string:sorted_member_ids>

**Parameters**:

* app_id: 应用的 id
* client_id: 登录时使用的 clientId
* sorted_member_ids: sorted_member_ids 是以半角冒号（:）分隔、升序排序 的 user id，即邀请参与该对话的成员列表

**Response** `200` ::

    {
      "timestamp":"1450167224.627163",
      "signature":"14bf896f77332d3569645632088feac8d4c70515",
      "nonce":"b3uMtwWT",
      "sorted_member_ids":"3:4:5:6",
      "app_id":"1",
      "client_id":"2"
    }

-- end


获取群组加人操作签名
~~~~~~~~~~~~~~~
**URL**::

    GET     /im/signature/invite/<string:app_id>/<string:client_id>/<string:conversation_id>/<string:sorted_member_ids>

**Parameters**:

* app_id: 应用的 id
* client_id: 登录时使用的 clientId
* conversation_id: 此次行为关联的对话 id
* sorted_member_ids: sorted_member_ids 是以半角冒号（:）分隔、升序排序 的 user id，即邀请参与该对话的成员列表；对加入群的情况，这里 sorted_member_ids 是空字符串。

**Response** `200` ::

    {
      "action":"invite",
      "signature":"c2610b002a8a9e20692f18e62b671dd4df47d9f5",
      "conversation_id":"3",
      "app_id":"1",
      "nonce":"QDFIkEMB",
      "sorted_member_ids":"4:5:6",
      "client_id":"2",
      "timestamp":"1450167393.275691"
    }

-- end


获取群组删人操作签名
~~~~~~~~~~~~~~~
**URL**::

    GET     /im/signature/kick/<string:app_id>/<string:client_id>/<string:conversation_id>/<string:sorted_member_ids>

**Parameters**:

* app_id: 应用的 id
* client_id: 登录时使用的 clientId
* conversation_id: 此次行为关联的对话 id
* sorted_member_ids: sorted_member_ids 是以半角冒号（:）分隔、升序排序 的 user id，即邀请参与该对话的成员列表

**Response** `200` ::

    {
      "action":"kick",
      "signature":"b765a66edb0d574f6c5bdf390eb79ee83cefece1",
      "conversation_id":"3",
      "app_id":"1",
      "nonce":"co0eRCXR",
      "sorted_member_ids":"4:5:6",
      "client_id":"2",
      "timestamp":"1450167470.05577"
    }

-- end


创建群组
~~~~~~~~~~~~~~~
**URL**::

    POST     /im/group

**Parameters**:

* group_name: 群组名称
* member_client_ids: member_client_ids 是以半角冒号（:）分隔的 client_id
* organization_id: 机构 id
* conversation_id:   会话 id (会话id为空时，后台会创建新的会话并分配到群组)
* group_avatar:    群组头像（上传文件后获取的完整路径）
* admin_uid:       管理员uid
* description:     群描述信息

备注：member_client_ids 和 admin_uid 中用户id采用 client_id, 即带字母前缀

**Response** `201` ::

    {
        "group_id": 13,
        "group_name":"666",
        "member_client_ids":"o12:u232:p23",
        "organization_id": 2,
        "conversation_id": "dasjfr4529sadfh",
        "group_avatar": "http://pic.hisihi.com/232rwfrqw.jpg",
        "admin_uid": "o12",
        "description": "群描述信息"
    }

-- end


更新群组信息
~~~~~~~~~~~~~~~
**URL**::

    PUT     /im/group/<int:group_id>

**Parameters**:

* group_name: 群组名称

**Response** `200` ::

    {
        "group_name":"g123"
    }
-- end


删除群组
~~~~~~~~~~~~~~~
**URL**::

    DELETE     /im/group/<int:group_id>

**Parameters**:

* N/A

**Response** `204`::
-- end


群主解散群
~~~~~~~~~~~~~~~
**URL**::

    DELETE     /im/user/<int:uid>/group/<int:group_id>

**Parameters**:

备注: uid 为 client_id, 即带字母前缀

**Response** `204`::
-- end


添加群成员
~~~~~~~~~~~~~~~
**URL**::

    POST     /im/group/<int:group_id>/member

**Parameters**:

* group_id: 群组id
* member_client_ids: member_client_ids 是以半角冒号（:）分隔的 client_id

备注: member_client_ids 中为 client_id, 即带字母前缀

**Response** `201` ::

    {
        "group_id":12,
        "member_client_ids":"c667:c775"
    }
-- end


删除群成员
~~~~~~~~~~~~~~~
**URL**::

    DELETE     /im/group/<int:group_id>/member/<string:client_id>

**Parameters**:

* group_id: 群组id
* client_id: IM 用户 client_id


**Response** `204` ::
-- end


获取机构下所有群组
~~~~~~~~~~~~~~~
**URL**::

    GET     /im/org/<int:organization_id>/groups

**Parameters**:

* organization_id: 机构id
* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

**Response** `200` ::

    {
        "data":[
            {
                "id":12,
                "group_avatar":"0",
                "group_name":"g123",
                "description":"",
                "level":1000,
                "conversation_id": "234fwrw23",
                "create_time":1450423535
            },
            {
                "id":13,
                "group_avatar":"0",
                "group_name":"676",
                "description":"",
                "level":1000,
                "conversation_id": "234fwrw23",
                "create_time":1450423856
            }
        ],
        "total_count":2
    }

-- end


获取所有机构的所有群组
~~~~~~~~~~~~~~~
**URL**::

    GET     /im/groups

**Parameters**:

* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

**Response** `200` ::

    {
        "data":[
            {
                "id":12,
                "group_avatar":"0",
                "group_name":"g123",
                "description":"",
                "level":1000,
                "conversation_id": "234fwrw23",
                "create_time":1450423535
            },
            {
                "id":13,
                "group_avatar":"0",
                "group_name":"676",
                "description":"",
                "level":1000,
                "conversation_id": "234fwrw23",
                "create_time":1450423856
            }
        ],
        "total_count":2
    }

-- end


获取所有联系人
~~~~~~~~~~~~~~~
**URL**::

    GET     /im/org/<int:organization_id>/contacts

**Parameters**:

* organization_id: 机构id

**Response** `200` ::

    {
        "data":[
            {
                "id":12,
                "avatar":"0",
                "name":"g123",
                "type":"group"
            },
            {
                "id":13,
                "avatar":"0",
                "name":"676",
                "type":"group"
            },
            {
                "id":529,
                "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-07-15/55a62d15b9fc4-05505543.jpg",
                "name":"LEE",
                "type":"user"
            }
        ]
    }

-- end


向班级群发消息(实际只是做标记)
~~~~~~~~~~~~~~~
**URL**::

    POST     /im/org/<int:class_id>/message

**Parameters**:

* class_id: 班级id

**Response** `201` ::

    {
        "class_id": 2,
        "push_history_record_id": 123
    }

-- end


获取用户的群组
~~~~~~~~~~~~~~~
**URL**::

    GET     /im/user/<string:client_id>/groups

**Parameters**:

* client_id: 用户的 client_id, 带前缀

**Response** `200` ::

    {
        "data":[
            {
                "id":11,
                "group_avatar":"0",
                "conversation_id":"",
                "group_name":"123",
                "organization_id":1,
                "description": "群组描述",
                "create_time": "创建时间戳",
                "level": 1000
            },
            {
                "id":12,
                "group_avatar":"0",
                "conversation_id":"5673c5ef60b27f7a2627062f",
                "group_name":"g123",
                "organization_id":2,
                "description": "群组描述",
                "create_time": "创建时间戳"
                "level": 1000
            }
        ]
    }

-- end


获取群组详情
~~~~~~~~~~~~~~~
**URL**::

    GET     /im/group/<int:group_id>?client_id=c001

**Parameters**:

* group_id: 群组 id
* client_id: 用户 IM id。如果传入该参数会返回用户是否在该群中，否则不返回

**Response** `200` ::

    {
        "is_exist_in_group": True,
        "data":{
            "group_member_info":[
                {
                    "is_admin":0,
                    "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-12-22/56792a426d0b5-05505543.jpg",
                    "nickname":"Leslie",
                    "client_id":"c72"
                }
            ],
            "group_info":{
                "create_time":1450423535,
                "description":"",
                "organization_id":2,
                "conversation_id":"5673c5ef60b27f7a2627062f",
                "id":12,
                "group_avatar":"0",
                "group_name":"g123",
                "level":1000
            }
        }
    }

-- end


用户加群申请
~~~~~~~~~~~~~~~
**URL**::

    POST     /im/user/<string:client_id>/group/<int:group_id>/join_group_notification

**Parameters**:

* client_id: 用户 client_id
* group_id:  群组 id

**Response** `201` ::

    {
        "message": "已为您提交加群申请"
    }

-- end
