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
      "total_count": 1,
      "data": [
        {
          "is_out_of_date": false,
          "end_time": 1464624000,
          "id": 1,
          "obtain_id": 6,
          "is_used": false,
          "course_name": "PS-01",
          "money": 200,
          "type": 1,
          "start_time": 1464105600
        }
      ]
    }
** end


用户领取优惠券
~~~~~~~~~~~~~~~
**URL**::

    POST     /user/coupons

**Parameters**:

* 必须登录
* teaching_course_id: 课程id
* coupon_id: 优惠券id

**Response** `201` ::

    {
      "coupon_id": "1",
      "id": 7,
      "promo_code": "0800001471609291",
      "promo_code_url": "http://pic.hisihi.com/2016-05-26/1464248500365467.png",
      "teaching_course_id": "24",
      "uid": 567
    }
    promo_code 为优惠码     promo_code_url为优惠码生成的二维码
** end


用户领取礼包
~~~~~~~~~~~~~~~
**URL**::

    POST     /user/gift_package

**Parameters**:

* uid: 用户id
* obtain_coupon_record_id: 用户领取优惠券记录的id
* name:  姓名
* phone_num:  电话
* address:  地址

**Response** `201` ::

    {
        "address": "1",
        "id": 1,
        "name": "1",
        "obtain_coupon_record_id": "1",
        "phone_num": "1",
        "uid": "1"
    }
** end


用户优惠券详情
~~~~~~~~~~~~~~~
**URL**::

    GET     /user/coupon/<int:id>/detail

**Parameters**:

* id: 优惠券列表里的id

**Response** `201` ::

    {
      "id": 1,
      "course_name": "UI-03",
      "end_time": 1464624000,
      "obtain_id": 6,
      "instructions_for_use": "本券限现场使用，每次限用一张；本券不可兑换现金",
      "is_out_of_date": false,
      "is_used": false,
      "money": 200,
      "promo_code": "0800001772654868",
      "promo_code_url": "http://pic.hisihi.com/2016-05-26/1464247184466871.png",
      "service_condition": "仅可购买@C++--从入门到放弃",
      "start_time": 1464105600,
      "type": 1,
      "using_method": "结算时手机出示此优惠券，请商家扫描二维码或输入号码，待验证成功后，即成功使用"
    }
** end