.. _student:

机构学生
==========

每日签到
~~~~~~~~~~~~~~~
**URL**::

    POST     /<int:oid>/student/<int:uid>/sign-in/<date>


**Parameters**:

* oid: 机构id号
* uid: 学生id号
* date: 日期，必须是今天,如'2015-12-09'

**Response** `202` ::

    {
        "code": 0,
        "msg": "ok",
        "request": "PUT  /v1/online/pv+1"
    }

**Memo**:

* 此接口必须拥有UserCSUScope权限，通常由hisihi 大众版 App扫描二维码调用
* 如果是通过大众版调用，则oid和date参数已经自动生成，只需要将学生的id号填入Url模板中即可