.. _order:

抵扣券订单
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
      "create_time": 1474510557,
      "id": 1,
      "mobile": "18600466074",
      "num": 1,
      "order_sn": "201609221015536363",
      "order_status": 0,
      "organization_id": 41,
      "price": 500,
      "rebate": {
        "courses_id": 60,
        "courses_name": "javascript 入门到放弃(6)",
        "courses_pic": "http://pic.hisihi.com/2016-09-06/1473157611724128.png",
        "id": 5,
        "is_out_of_date": 0,
        "is_use": 0,
        "rebate_name": "我是抵扣券",
        "rebate_text": "500元抵扣券抵10000元学费",
        "use_end_time": 1478327940,
        "use_start_time": 1474353540,
        "user_rebate_id": 0
      },
      "uid": 72
    }

结果说明：
* create_time: 下单时间
* order_sn: 订单号
* order_status: 订单状态，0待付款，1已付款，2已使用，3已评价
* price: 订单金额
* num: 抵扣券数量
* rebate_id: 抵扣券id


用户订单列表
~~~~~~~~~~~~~~~
**URL**::

    GET order/list?page=1&per_page=10

**Parameters**:

* page: 页码
* per_page: 每页数量

**Response** `200` ::

    [
      {
          "create_time": 1474510557,
          "id": 1,
          "mobile": "18600466074",
          "num": 1,
          "order_sn": "201609221015536363",
          "order_status": 0,
          "organization_id": 41,
          "price": 500,
          "rebate": {
            "courses_id": 60,
            "courses_name": "javascript 入门到放弃(6)",
            "courses_pic": "http://pic.hisihi.com/2016-09-06/1473157611724128.png",
            "id": 5,
            "is_out_of_date": 0,
            "is_use": 0,
            "rebate_name": "我是抵扣券",
            "rebate_text": "500元抵扣券抵10000元学费",
            "use_end_time": 1478327940,
            "use_start_time": 1474353540,
            "user_rebate_id": 0
          },
          "uid": 72
        }
    ]


订单详情
~~~~~~~~~~~~~~~
**URL**::

    GET order/detail/<int:oid>

**Parameters**:

* oid: 订单id


**Response** `200` ::

    {
      "create_time": 1474510557,
      "id": 1,
      "mobile": "18600466074",
      "num": 1,
      "order_sn": "201609221015536363",
      "order_status": 0,
      "organization_id": 41,
      "price": 500,
      "rebate": {
        "courses_id": 60,
        "courses_name": "javascript 入门到放弃(6)",
        "courses_pic": "http://pic.hisihi.com/2016-09-06/1473157611724128.png",
        "id": 5,
        "is_out_of_date": 0,
        "is_use": 0,
        "rebate_name": "我是抵扣券",
        "rebate_text": "500元抵扣券抵10000元学费",
        "use_end_time": 1478327940,
        "use_start_time": 1474353540,
        "user_rebate_id": 0
      },
      "uid": 72
    }

**结果说明**:
* courses_pic: 课程图片
* rebate_name: 抵扣券名称
* rebate_text: 优惠方案
* use_end_time: 有效期开始时间
* use_start_time: 有效期结束时间
* is_use: 是否已使用,0未使用，1已使用
* is_out_of_date: 是否已过期,0未过期，1已过期
* order_status: 订单状态，0待付款，1已付款，2已使用，3已评价
