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
        "qq": "117287879",
        "content": "闪退"
    }

**Parameters**:

* organization_id：机构的ID
* qq：QQ号
* content: 反馈内容
Response Status `201` :