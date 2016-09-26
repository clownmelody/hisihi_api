.. _pay:

支付相关
=========

统一支付订单
~~~~~~~~~~~~~~~~~~~~~~~
**URL**::

    GET     pay/create/pay/<int:oid>/<int:type>

**Parameters**:

* oid: 订单id
* type: 支付类型,0微信支付，1支付宝支付


**Response** `200` ::

    订单已支付返回结果：
    {
      "pay_status": 1,
      "user_rebate_id": 2
    }

    微信调用成功返回结果：
    {
      "appid": "wx9dcbe8acfcac3740",
      "noncestr": "jRdtzOTD8dBBk9cUVQixC5G4RhHwWrRw",
      "package": "Sign=WXPay",
      "partnerid": "1392378802",
      "pay_status": 0,
      "prepayid": "wx201609261152180f8256ae9d0049337449",
      "sign": "E7C64668CE5253A000951837B57D86E4",
      "timestamp": 1474861950
    }
**Error_Code** ::
* 10001: 创建订单失败
* 10003: 获取用户抵扣券失败