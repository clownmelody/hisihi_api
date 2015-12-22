.. _feedback:

反馈
=============
    提交机构APP反馈信息

提交机构APP反馈信息
~~~~~~~~~~~~~~~~~~~~
URL::

    POST     org/feedback/advice

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