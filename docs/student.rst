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
      "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b325d2dd7-05505543.jpg",
      "class_group": "Python\u57f9\u8bad\u4e00\u73ed",
      "course_name": "UI\u8bbe\u8ba1",
      "graduation_status": 2,
      "sign_in_count": 0,
      "student_name": "\u8d75\u864e",
      "uid": 566
    }

** end **


获取学生历史签到记录
~~~~~~~~~~~~~~~
**URL**::

    GET     /student/<int:uid>/sign-in/history

**Parameters**:

* uid: 学生id号
* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

**Response** `200` ::

    {
        "sign_in_history":[
            {
                "is_sign_in":true,
                "date":"2015-12-08",
                "uid":565
            },
            {
                "is_sign_in":false,
                "date":"2015-12-09",
                "uid":565
            }
        ],
        "total_count":2
    }

** end **


获取学生所属分组列表
~~~~~~~~~~~~~~~~~~~~
**URL**::

    GET     /student/<int:uid>/class/<int:oid>/in

**Parameters**:

* uid: 学生id号
* oid: 机构id号

**Response** `200` ::

    {
        "class_list":[
            {
                "class_id":1,
                "in_this_class":true,
                "class_name":"UI设计三班"
            },
            {
                "class_id":2,
                "in_this_class":false,
                "class_name":"Python培训一班"
            },
            {
                "class_id":3,
                "in_this_class":false,
                "class_name":"PHP培训二班"
            }
        ],
        "total_count":3
    }

** end *


修改学生所属分组
~~~~~~~~~~~~~~~~~~~~
**URL**::

    PUT     org/student/<int:uid>/class/<int:class_id>/move

**Parameters**:

* uid: 学生id号
* class_id: 新分组id

**Response** `202` ::

    {
        "class_id": 2,
        "uid": 565
    }

** end *


修改学生毕业状态
~~~~~~~~~~~~~~~~~~~~
**URL**::

    PUT     org/student/<int:uid>/graduation/<int:class_id>/status/<int:status>

**Parameters**:

* uid: 学生id号
* class_id: 所属班级id
* status: 毕业状态值，1-未毕业，2-已毕业

**Response** `202` ::

    {
      "class_id": 2,
      "status": 3,
      "uid": 190
    }

** end *