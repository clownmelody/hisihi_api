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
      "info": "提交订单成功",
      "order": {
        "courses_id": 60,
        "create_time": 1474510557,
        "id": 1,
        "mobile": "18600466074",
        "order_sn": "201609221015536363",
        "order_status": 0,
        "organization_id": 41,
        "pay_status": 0,
        "pay_time": null,
        "pay_type": null,
        "price": 500,
        "rebate_id": 5,
        "rebate_num": 1,
        "status": 0,
        "uid": 72
      }
    }

结果说明：
* create_time: 下单时间
* order_sn: 订单号
* order_status: 订单状态，0待使用，1已使用，2已领取
* pay_status: 支付状态，0未支付，1已支付
* pay_time: 支付时间
* pay_type: 支付方式，0微信支付，1支付宝支付
* price: 订单金额
* rebate_num: 抵扣券数量
* rebate_id: 抵扣券id


用户订单列表
~~~~~~~~~~~~~~~
**URL**::

    GET order/list

**Response** `200` ::

    [
      {
        "courses_id": 60,
        "courses_name": "javascript 入门到放弃(6)",
        "courses_pic": "http://pic.hisihi.com/2016-09-06/1473157611724128.png",
        "create_time": 1474510557,
        "id": 1,
        "mobile": "18600466074",
        "num": 1,
        "order_sn": "201609221015536363",
        "order_status": 0,
        "pay_status": 0,
        "price": 500,
        "rebate_id": 5,
        "rebate_name": "我是抵扣券",
        "uid": 72
      }
    ]


订单详情
~~~~~~~~~~~~~~~
**URL**::

    GET order/list

**Response** `200` ::

    {
      "courses_id": 60,
      "courses_name": "javascript 入门到放弃(6)",
      "courses_pic": "http://pic.hisihi.com/2016-09-06/1473157611724128.png",
      "create_time": 1474510557,
      "id": 1,
      "mobile": "18600466074",
      "num": 1,
      "order_sn": "201609221015536363",
      "order_status": 0,
      "pay_status": 0,
      "price": 500,
      "rebate_id": 5,
      "rebate_name": "我是抵扣券",
      "rebate_text": "500元抵扣券抵10000元学费",
      "uid": 72,
      "use_end_time": 1478327940,
      "use_start_time": 1474353540
    }
结果说明：
* courses_pic: 课程图片
* rebate_name: 抵扣券名称
* rebate_text: 优惠方案
* use_end_time: 有效期开始时间
* use_start_time: 有效期结束时间
