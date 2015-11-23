.. _sms:

v1/sms
========

发送验证码短信
~~~~~~~~~~~~~~~

**URL**::

    POST   /verify

**POST Simple**

.. sourcecode:: json

    {
        "mobile": "18678789877"
    }

**Parameters**:

* mobile：需要发送验证码的手机号

**Response** `201`:

.. sourcecode:: json

    {
        "smsId": 1232222
    }