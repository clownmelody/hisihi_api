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
      "create_time": 1474534657,
      "id": 3,
      "mobile": "18600466074",
      "num": 1,
      "order_sn": "201609221657379606",
      "order_status": 0,
      "price": 200,
      "rebate": {
        "courses_id": 52,
        "courses_name": "哈哈哈",
        "courses_pic": "http://pic.hisihi.com/2016-06-22/1466589018729417.png",
        "is_out_of_date": 0,
        "is_use": 0,
        "rebate_id": 2,
        "rebate_name": "还是辣鸡",
        "rebate_text": "200元抵扣券抵2000元学费",
        "use_end_time": 1475309400,
        "use_start_time": 1474618200
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
        "create_time": 1474534427,
        "id": 2,
        "mobile": "18600466074",
        "num": 1,
        "order_sn": "201609221653472174",
        "order_status": 0,
        "price": 100,
        "rebate": {
          "courses_id": 30,
          "courses_name": "手绘测试",
          "courses_pic": "http://pic.hisihi.com/2016-06-02/1464838896954120.png",
          "is_out_of_date": 0,
          "is_use": 0,
          "rebate_id": 3,
          "rebate_name": "就是辣鸡",
          "rebate_text": "100元抵扣券抵1000元学费",
          "use_end_time": 1475050260,
          "use_start_time": 1474618260
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
      "price": 500,
      "rebate": {
        "courses_id": 60,
        "courses_name": "javascript 入门到放弃(6)",
        "courses_pic": "http://pic.hisihi.com/2016-09-06/1473157611724128.png",
        "is_out_of_date": 0,
        "is_use": 0,
        "rebate_id": 5,
        "rebate_name": "我是抵扣券",
        "rebate_text": "500元抵扣券抵10000元学费",
        "use_end_time": 1478327940,
        "use_start_time": 1474353540
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
