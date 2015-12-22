.. _feedback:

反馈
=============
    表示商城类资源

进入商城
~~~~~~~~~~~~~~~~~~~~
URL::

    POST     org/feedback/post

**POST Sample**：

.. sourcecode:: json

    {
        "organization_id": "3",
        "admin_id": "2",
        "qq": "117287879",
        "content": "闪退"
    }

**Parameters**:

* organization_id：机构的ID
* admin_id: 机构管理员ID
* qq：QQ号
* content: 反馈内容
Response Status `201` :

** end *