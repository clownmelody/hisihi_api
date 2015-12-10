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

获取学生资料
~~~~~~~~~~~~~~~
**URL**::

    GET     /student/<int:uid>/profile

**Parameters**:

* uid: 学生id号

**Response** `200` ::

    {
          "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b11e133f0-05505543.jpg",
          "class_group": "Python\u57f9\u8bad\u4e00\u73ed",
          "course_name": "\u4e0a\u5e02\u5927\u516c\u53f8",
          "sign_in_count": 1,
          "status": 1,
          "student_name": "\u674e\u4e8c\u72d7",
          "uid": 565
    }
** end **


获取学生历史签到记录
~~~~~~~~~~~~~~~
**URL**::

    GET     /student/<int:uid>/sign-in/history

**Parameters**:

* uid: 学生id号

**Response** `200` ::

    [
        {
            "organization_id":2,
            "sign_in_time":"2015-12-09",
            "uid":2
        },
        {
            "organization_id":2,
            "sign_in_time":"2015-12-07",
            "uid":2
        },
        {
            "organization_id":2,
            "sign_in_time":"2015-12-03",
            "uid":2
        }
    ]

** end **