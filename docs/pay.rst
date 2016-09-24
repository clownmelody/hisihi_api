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

    {
      "appid": "wx9dcbe8acfcac3740",
      "mch_id": "1392378802",
      "nonce_str": "obbxtwtSeIGcTg17",
      "prepay_id": "wx20160924172118be70f5e9240487045014",
      "result_code": "SUCCESS",
      "return_code": "SUCCESS",
      "return_msg": "OK",
      "sign": "99F51B8E3D09D291C519EA50190FF2B2",
      "trade_type": "APP"
    }


