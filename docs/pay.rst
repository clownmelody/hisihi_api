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

    支付宝调用成功返回：
    {
      "data": "_input_charset=\"UTF-8\"&body=\"heishehui.cn\"&notify_url=\"http://dev.api.hisihi.com/v1/pay/alipay/notify\"&out_trade_no=\"201609241603186115\"&partner=\"2088321008674225\"&paymnet_type=\"1\"&seller_id=\"523453004@qq.com\"&service=\"mobile.securitypay.pay\"&subject=\"抵扣券\"&total_fee=\"0.01\"&sign=\"C59Sc2C6GmRX6FBjOoSPKI+N4+OGEU35bElXcOiA5m74N88Fwybhkar28WEUlBkdofrLeaz+9eZvzUBYn7lYoKLAvbDYRFBmc+cBB0p/9Zvrj3YOkQVKOKgEyJyCD4Uz4qAUJcKJ/nPca/mOnS74Ya6t4yAHKQezz0EXxWxMCaw=\"&sign_type=\"RSA\""
    }
**Error_Code** ::
* 10001: 创建订单失败
* 10003: 获取用户抵扣券失败
* 10004: 抵扣券已过期
* 10006: 抵扣券已失效


支付状态查询
~~~~~~~~~~~~~~~~~~~~~~~
**URL**::

    GET     pay/order/query/<int:oid>

**Parameters**:

* oid: 订单id


**Response** `200` ::

    订单已支付返回结果：
    {
      "pay_status": 1,
      "user_rebate_id": 2
    }
**结果说明** ::
* pay_status: 支付状态，0未支付，1已支付，2正在支付中

**Error_Code** ::


