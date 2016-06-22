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
          "start_time": 1464105600,
          "is_invalid": false
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
      "has_obtained": false,
      "obtain_id": 14
    }

    obtain_id 为优惠码领取记录id，用于获取优惠券详情
    has_obtained表示优惠券是否已经领取过，true为已经领取过，false表示第一次领取
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

* id: 领取记录obtain_id

**Response** `201` ::

    {
      "course_name": "javascript 入门到放弃（5）",
      "end_time": 1464624000,
      "id": 2,
      "instructions_for_use": "本券限现场使用，每次限用一张；本券不可兑换现金",
      "is_obtain_gift_package": 0,
      "is_out_of_date": false,
      "is_used": false,
      "money": 400,
      "obtain_id": 12,
      "promo_code": "0800004906247644",
      "promo_code_url": "http://pic.hisihi.com/2016-05-27/1464338164107386.png",
      "service_condition": "仅可购买课程@javascript 入门到放弃（5）",
      "start_time": 1464105600,
      "type": 1,
      "using_method": "结算时手机出示此优惠券，请商家扫描二维码或输入号码，待验证成功后，即成功使用"
    }

    is_obtain_gift_package有三种状态，0表示未领取礼包未验证二维码，1表示未领取礼包已验证二维码，2表示已领取礼包
        0和1两种状态下都可以领取礼包
** end


用户优惠券详情（v2.9.2版本）
~~~~~~~~~~~~~~~
**URL**::

    GET     /user/coupon/<int:id>/detail

**Parameters**:

* version: 2.92
* id: 领取记录obtain_id

**Response** `200` ::

    {
        "course_id":3,
        "course_name":"PS-01",
        "customer_service_telephone_number":"4000340033",
        "end_time":1466006399,
        "gift_package_info":{
            "detail":"送wecom1280元数位板一个，200元马克笔一套",
            "id":1,
            "introduce":"报名成功即可领取wacom数位板一套"
        },
        "id":1,
        "instructions_for_use":"",
        "is_obtain_gift_package":0,
        "is_out_of_date":true,
        "is_used":false,
        "money":200,
        "obtain_id":45,
        "organization_info":{
            "advantage":"环境相当优越#go kb#上市大公司",
            "city":"湖北省 武汉市",
            "guarantee_num":200,
            "id":41,
            "introduce":"测试",
            "latitude":null,
            "location":"洪山区野芷湖西路你懂的",
            "logo":"http://pic.hisihi.com/2016-05-23/1463985032967582.jpg@17-102-542-542a",
            "longitude":null,
            "name":"英雄联盟开黑组",
            "phone_num":"145632145632",
            "slogan":"",
            "type":32,
            "video":"70",
            "video_img":"http://pic.hisihi.com/2016-04-30/572416c5971ac.JPG",
            "view_count":5595
        },
        "promo_code":"0800004905599549",
        "promo_code_url":"http://wechat.hisihi.com/online/index.php/scissor/index/index?coupon=0800004905599549",
        "service_condition":"",
        "start_time":1464105600,
        "type":1,
        "using_method":""
    }
** end