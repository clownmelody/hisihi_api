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

    微信返回结果：
    {
      "appid": "wx9dcbe8acfcac3740",
      "noncestr": "oYaEvh3oZrbuIJPVaXcItMiB2LBaQnz0",
      "package": "Sign=WXPay",
      "partnerid": "1392378802",
      "prepayid": "wx20160924194638b628a487960185021418",
      "sign": "D5BF86A210D846C4D7E03E9F8D335354",
      "timestamp": 1474717600
    }

**Error_Code** ::
* 10001: 创建订单失败
* 11001: 订单已经支付