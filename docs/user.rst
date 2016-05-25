.. _user:

用户
=============

创建机构管理员
~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    POST      /org/admin

**POST Sample**：

.. sourcecode:: json

    {
        "mobile": "18677771949",
        "sms_code": "567663",
        "password": "hiyouth"
    }

**Parameters**:

* mobile：手机号（注册账号）
* sms_code: 短信验证码（需要开发者首先调用 :ref:`短信发送` <sms>`
* password: 用户密码

**Response** `201`:

.. sourcecode:: json

    {
        "id": 3,
        "username": "网易"
        "mobile": "18698768787"
        'create_time": "1456878787"
    }


重置机构管理员密码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    PUT     org/admin/password

**PUT Sample**:

.. sourcecode:: json

    {
        "mobile": "18677771949",
        "sms_code": "567663",
        "password": "hiyouth",
        "type": "300"
    }

**Parameters**:

* mobile：手机号（注册账号）
* sms_code: 短信验证码（需要开发者首先调用 :ref:`短信发送` <sms>`
* password: 用户新密码
* type: 账号类型，可取值参见 :ref:`枚举类型说明 <enums>`

**Response Sample** `202`:

.. sourcecode:: json

    {
        "code": 0,
        "msg": "ok",
        "request": "PUT v1/org/admin/password"
    }


获取用户优惠券列表
~~~~~~~~~~~~~~~
**URL**::

    GET     /user/<int:uid>/coupons

**Parameters**:

* uid: 用户id

**Response** `200` ::

    {
        "total_count":1,
        "data":[
            {
                "id":1,
                "end_time":1464624000,
                "money":200,
                "type":1,
                "start_time":1464105600,
                "is_used":false,
                "is_out_of_date": false,
                "course_name":"nodejs全栈式开发"
            }
        ]
    }
** end


用户领取优惠券
~~~~~~~~~~~~~~~
**URL**::

    POST     /user/coupons

**Parameters**:

* uid: 用户id
* coupon_id: 优惠券id

**Response** `200` ::

    {
      "coupon_id": "2",
      "id": 2,
      "uid": "72"
    }
