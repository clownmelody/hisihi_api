.. _webSites:

微信验证优惠券
=========

验证机构admin账号
~~~~~~~~~~~~~~~~~~~~~~~
**URL**::

    POST org/verify/org/admin

**Parameters**:

* account:  账号
* secret:  密码

**Response** `200` ::

    {
      "admin_id": 2,
      "org": {
        "application_status": 2,
        "id": 57,
        "logo": "http://pic.hisihi.com/2016-04-05/5703249a54993.png",
        "name": "武汉测试测试机构"
      }
    }

**Explain**:
    admin_id                管理员账号记录id
    application_status      机构审核状态，1未审核，2已审核

    状态码1005表示验证失败
-- end


绑定机构帐号和微信号
~~~~~~~~~~~~~~~
**URL**::

    POST org/admin/bind/weixin

**Parameters**:

* organization_id:  机构管理员账号记录id
* admin_id:  机构管理员账号记录id
* weixin_account: 微信帐号
* weixin_nickname:  微信昵称
* weixin_avatar:  微信头像


**Response** `201` ::

    {
      "organization_id":"41",
      "admin_id": "2",
      "id": 1,
      "weixin_account": "oh03Xs4rFTwohwvjrA5ehtFqBeRg",
      "weixin_avatar": " http://127.0.0.1:5000/v1/org/verify/org/admin",
      "weixin_nickname": "Jimmy"
    }

-- end


验证优惠码
~~~~~~~~~~~~~~~
**URL**::

    POST org/admin/verify/coupon/code

**Parameters**:

* weixin_account: 微信帐号
* coupon_code:  优惠码

**Response** `202` ::

    {
      "has_teaching_course": true,
      "is_bind": true,
      "is_out_of_date": false,
      "is_used": true,
      "is_verify": true
    }

-- end