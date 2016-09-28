.. _order:

抵扣券相关
=========

提交订单
~~~~~~~~~~~~~~~~~~~~~~~
**URL**::

    POST order/create

**POST Sample**：

.. sourcecode:: json

    {
        "mobile":"18600466074",
        "courses_id":60,
        "rebate_id":5,
        "num":1
    }

**Parameters**:

* mobile: 手机号
* courses_id: 课程id
* rebate_id: 抵扣券id
* num: 购买数量


**Response** `201` ::

    {
      "create_time": 1474534427,
      "id": 2,
      "mobile": "18600466074",
      "num": 1,
      "order_sn": "201609221653472174",
      "order_status": 0,
      "organization_id": 41,
      "price": 100,
      "rebate": {
        "courses_id": 30,
        "courses_name": "手绘测试",
        "courses_pic": "http://pic.hisihi.com/2016-06-02/1464838896954120.png",
        "id": 3,
        "is_out_of_date": 0,
        "is_use": 0,
        "name": "就是辣鸡",
        "rebate_text": "100元抵扣券抵1000元学费",
        "use_end_time": 1475050260,
        "use_start_time": 1474618260,
        "user_rebate_id": 0,
        "organization_id": 41,
        "is_disabled": 1
      },
      "uid": 72
    }

结果说明：
* create_time: 下单时间
* order_sn: 订单号
* order_status: 订单状态，0待付款，1已付款，2已使用，3已评价
* price: 订单金额
* num: 抵扣券数量
* id: 抵扣券id
* user_rebate_id: 用户抵扣券id，0表示还未生成，用于调用抵扣券详情接口
* is_disabled: 抵扣券是否失效，0未失效，1已失效

**Error_code**::
* 5000: 未找到对应机构
* 10001: 创建订单失败
* 10004: 抵扣券已过期


用户订单列表
~~~~~~~~~~~~~~~
**URL**::

    GET order/list?page=1&per_page=10

**Parameters**:

* page: 页码
* per_page: 每页数量

**Response** `200` ::

    {
      "count": 3,
      "data": [
        {
          "create_time": 1474534657,
          "id": 3,
          "mobile": "18600466074",
          "num": 1,
          "order_sn": "201609221657379606",
          "order_status": 0,
          "organization_id": 48,
          "price": 200,
          "rebate": {
            "courses_id": 52,
            "courses_name": "哈哈哈",
            "courses_pic": "http://pic.hisihi.com/2016-06-22/1466589018729417.png",
            "id": 2,
            "is_out_of_date": 0,
            "is_use": 0,
            "name": "还是辣鸡",
            "rebate_text": "200元抵扣券抵2000元学费",
            "use_end_time": 1475309400,
            "use_start_time": 1474618200,
            "user_rebate_id": 0,
            "organization_id": 41,
            "is_disabled": 1
          },
          "uid": 72
        },
        {
          "create_time": 1474534427,
          "id": 2,
          "mobile": "18600466074",
          "num": 1,
          "order_sn": "201609221653472174",
          "order_status": 0,
          "organization_id": 41,
          "price": 100,
          "rebate": {
            "courses_id": 30,
            "courses_name": "手绘测试",
            "courses_pic": "http://pic.hisihi.com/2016-06-02/1464838896954120.png",
            "id": 3,
            "is_out_of_date": 0,
            "is_use": 0,
            "name": "就是辣鸡",
            "rebate_text": "100元抵扣券抵1000元学费",
            "use_end_time": 1475050260,
            "use_start_time": 1474618260,
            "user_rebate_id": 0,
            "organization_id": 41,
            "is_disabled": 1
          },
          "uid": 72
        }
      ]
    }


订单详情
~~~~~~~~~~~~~~~
**URL**::

    GET order/detail/<int:oid>

**Parameters**:

* oid: 订单id


**Response** `200` ::

    {
      "create_time": 1474534427,
      "id": 2,
      "mobile": "18600466074",
      "num": 1,
      "order_sn": "201609221653472174",
      "order_status": 0,
      "organization_id": 41,
      "price": 100,
      "rebate": {
        "courses_id": 30,
        "courses_name": "手绘测试",
        "courses_pic": "http://pic.hisihi.com/2016-06-02/1464838896954120.png",
        "id": 3,
        "is_out_of_date": 0,
        "is_use": 0,
        "name": "就是辣鸡",
        "rebate_text": "100元抵扣券抵1000元学费",
        "use_end_time": 1475050260,
        "use_start_time": 1474618260,
        "user_rebate_id": 0,
        "organization_id": 41,
        "is_disabled": 1
      },
      "uid": 72
    }

**结果说明**:
* courses_pic: 课程图片
* name: 抵扣券名称
* rebate_text: 优惠方案
* use_end_time: 有效期开始时间
* use_start_time: 有效期结束时间
* is_use: 是否已使用,0未使用，1已使用
* is_out_of_date: 是否已过期,0未过期，1已过期
* order_status: 订单状态，0待付款，1已付款，2已使用，3已评价
* user_rebate_id: 用户抵扣券id，0表示还未生成，用于调用抵扣券详情接口



用户抵扣券列表
~~~~~~~~~~~~~~~
**URL**::

    GET user/<int:uid>/rebate/<int:type>?page=1&per_page=10

**Parameters**:

* uid: 用户id
* type: 类型，0表示未使用，1表示已失效，包含过期和已使用的
* page: 页码
* per_page: 每页数量


**Response** `200` ::

    {
      "data": [
        {
          "rebate_value": 1000,
          "name": "就是辣鸡",
          "courses_name": "手绘测试",
          "courses_id": 30,
          "use_end_time": 1474473600,
          "courses_pic": "http://pic.hisihi.com/2016-06-02/1464838896954120.png",
          "use_start_time": 1474618260,
          "is_out_of_date": 1,
          "user_rebate_id": 2,
          "is_obtain_gift_package": 0,
          "is_bind_gift_package": 1,
          "id": 3,
          "value": 100,
          "is_use": 0
        }
      ],
      "count": 1
    }

**结果说明**:
* courses_pic: 课程图片
* name: 抵扣券名称
* use_end_time: 有效期开始时间
* use_start_time: 有效期结束时间
* is_use: 是否已使用,0未使用，1已使用
* is_out_of_date: 是否已过期,0未过期，1已过期
* user_rebate_id: 用户抵扣券id，0表示还未生成，用于调用抵扣券详情接口
* is_obtain_gift_package: 是否领取礼包,0未领取，1已领取
* value: 抵扣券金额
* rebate_value: 抵扣券抵扣的金额
* is_bind_gift_package: 抵扣券是否绑定礼包，0未绑定，1绑定


抵扣券详情
~~~~~~~~~~~~~~~
**URL**::

    GET user/rebate/<int:id>/detail

**Parameters**:

* id: 用户抵扣券id，user_rebate_id


**Response** `200` ::

    {
      "is_out_of_date": 0,
      "promo_code": "0800000726408296",
      "value": 500,
      "order_id": 1,
      "id": 5,
      "is_use": 1,
      "customer_service_telephone_number": "4000340033",
      "user_rebate_id": 1,
      "rebate_value": 10000,
      "use_condition": "且前期费",
      "is_obtain_gift_package": 0,
      "use_method": "请问发给为爱人",
      "name": "我是抵扣券",
      "use_end_time": 1478327940,
      "organization_id": 41,
      "gift_package_info": {
        "id": 2,
        "detail": "送wecom1280元数位板一个",
        "introduce": "报名成功即可领取wacom数位板一个"
      },
      "use_instruction": "去放弃而过去发",
      "courses_name": "javascript 入门到放弃(6)",
      "promo_code_url": "http://wechat.hisihi.com/online/index.php/scissor/index/index?coupon=0800000726408296",
      "use_start_time": 1474353540,
      "courses_id": 60,
      "courses_pic": "http://pic.hisihi.com/2016-09-06/1473157611724128.png"
    }

**结果说明**:
* courses_pic: 课程图片
* name: 抵扣券名称
* use_end_time: 有效期开始时间
* use_start_time: 有效期结束时间
* is_use: 是否已使用,0未使用，1已使用
* is_out_of_date: 是否已过期,0未过期，1已过期
* user_rebate_id: 用户抵扣券id，0表示还未生成，用于调用抵扣券详情接口
* is_obtain_gift_package: 是否领取礼包,0未领取，1已领取
* value: 抵扣券金额
* rebate_value: 抵扣券抵扣的金额


领取抵扣券礼包
~~~~~~~~~~~~~~~
**URL**::

    POST user/rebate/gift_package

**POST Sample**：

.. sourcecode:: json

    {
        "uid":72,
        "user_rebate_id":1,
        "name":"航航",
        "phone_num":"18600466074",
        "address":"马湖商业街",
        "voucher":"http://pic.hisihi.com/2016-06-28/1467095297745554.jpg,http://pic.hisihi.com/2016-06-28/1467095295418991.jpg"
    }

**Parameters**:

* user_rebate_id: 用户抵扣券id
* uid: 用户id
* name: 用户姓名
* phone_num: 用户电话
* address: 用户地址
* voucher: 上传凭证，多图片地址逗号隔开


**Response** `200` ::

    {
      "address": "马湖商业街",
      "check": 0,
      "id": 1,
      "name": "航航",
      "phone_num": "18600466074",
      "uid": 72,
      "user_rebate_id": 1,
      "voucher": "http://pic.hisihi.com/2016-06-28/1467095297745554.jpg,http://pic.hisihi.com/2016-06-28/1467095295418991.jpg"
    }

**结果说明**:
* check: 审核状态，0未审核，1已审核，2已发放
