.. _im:

IM
==========

获取登陆操作签名
~~~~~~~~~~~~~~~
**URL**::

    GET     /signature/login/<string:app_id>/<string:client_id>

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

    GET     /signature/conversion/<string:app_id>/<string:client_id>/<string:sorted_member_ids>

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

    GET     /signature/invite/<string:app_id>/<string:client_id>/<string:conversion_id>/<string:sorted_member_ids>

**Parameters**:

* app_id: 应用的 id
* client_id: 登录时使用的 clientId
* conversion_id: 此次行为关联的对话 id
* sorted_member_ids: sorted_member_ids 是以半角冒号（:）分隔、升序排序 的 user id，即邀请参与该对话的成员列表；对加入群的情况，这里 sorted_member_ids 是空字符串。

**Response** `200` ::

    {
      "action":"invite",
      "signature":"c2610b002a8a9e20692f18e62b671dd4df47d9f5",
      "conversion_id":"3",
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

    GET     /signature/kick/<string:app_id>/<string:client_id>/<string:conversion_id>/<string:sorted_member_ids>

**Parameters**:

* app_id: 应用的 id
* client_id: 登录时使用的 clientId
* conversion_id: 此次行为关联的对话 id
* sorted_member_ids: sorted_member_ids 是以半角冒号（:）分隔、升序排序 的 user id，即邀请参与该对话的成员列表

**Response** `200` ::

    {
      "action":"kick",
      "signature":"b765a66edb0d574f6c5bdf390eb79ee83cefece1",
      "conversion_id":"3",
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

**Response** `201` ::

    {
        "group_id": 13,
        "group_name":"666",
        "member_client_ids":"o12:u232:p23"
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


添加群成员
~~~~~~~~~~~~~~~
**URL**::

    POST     /im/group/<int:group_id>/member

**Parameters**:

* group_id: 群组id
* member_client_ids: member_client_ids 是以半角冒号（:）分隔的 client_id

**Response** `201` ::

    {
        "group_id":12,
        "member_client_ids":"667:775"
    }
-- end


删除群成员
~~~~~~~~~~~~~~~
**URL**::

    DELETE     /im/group/<int:group_id>/member

**Parameters**:

* group_id: 群组id
* member_client_ids: member_client_ids 是以半角冒号（:）分隔的 client_id

**Response** `204` ::
-- end

