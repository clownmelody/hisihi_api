.. _classmate:

班级
===========

获取指定班级学生在指定日期的签到情况
~~~~~~~~~~~

**URL**::

    GET      org/<int:oid>/class/<int:cid>/sign-in/<date>/detail

**Parameters**:

* oid: 机构id号
* cid: 班级号
* data: 日期  格式为 2015-12-11
* page: 页数，默认值为1
* per_page: 每页记录数, 默认值为20

**Response** `200` ::

    {
        "data":[
            {
                "sign_in_status":true,
                "avatar":"http://wx.qlogo.cn/mmopen/zx5ksGgvtY3iadebad7OwiaYMdvKWjqDRzzlbLDcibicPlp6F37X2J7dHibyvhYTNqpv2LI4bREHneLvzLYRGVYcFlAJToQr2RKKF/0",
                "nickname":"李长椿",
                "uid":588
            },
            {
                "sign_in_status":false,
                "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b11e133f0-05505543.jpg",
                "nickname":"李长春",
                "uid":565
            }
        ],
        "sign_in_count": 1,
        "unsign_in_count": 1,
        "total_count":2
    }

-- end


获取指定班级所有学生uid
~~~~~~~~~~~

**URL**::

    GET      org/<int:oid>/class/<int:cid>/students

**Parameters**:

* oid: 机构id号
* cid: 班级号
* page: 页数，默认值为1
* per_page: 每页记录数, 默认值为20

**Response** `200` ::

    {
        "total_count":2,
        "data":[
            {
                "uid":567,
                "nickname":"哈哈",
                "avatar":null
            },
            {
                "uid":103,
                "nickname":"皮卡Q",
                "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-07-17/55a8aef4d0f65-05505543.jpg"
            }
        ]
    }

-- end


获取机构的班级列表
~~~~~~~~~~~

**URL**::

    GET      org/<int:oid>/class

**Parameters**:

* oid: 机构id号
* page: 页数，默认值为1
* per_page: 每页记录数, 默认值为20

**Response** `200` ::



    {
        "data":
        [
            {
                "student_count": 1,
                "class_time": "周一上、周二上晚、周三晚、周四上、周五下、周六上、周日无",
                "name": "UI设计三班",
                "id": 1
            },
            {
                "student_count": 1,
                "class_time": "周一无、周二无、周三无、周四无、周五无、周六无、周日无",
                "name": "Python培训一班",
                "id": 2
            },
            {
                "student_count": 0,
                "class_time": "周一无、周二无、周三无、周四无、周五无、周六无、周日无",
                "name": "PHP培训二班",
                "id": 3
            }
        ],
        "total_count": 3
    }

-- end


获取机构所有报名的学生
~~~~~~~~~~~

**URL**::

    GET      org/<int:oid>/enroll/student

**Parameters**:

* oid: 机构id号
* name: 学生名字或电话,模糊查询；默认None，查询全部

**Response** `200` ::



    {
        "total_count": 3,
        "data":
        [
            {
                "nickname": "孔二狗",
                "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-05-14/5554bdb720f29-05505543.jpg",
                "uid": 86
            },
            {
                "nickname": "赵虎",
                "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b325d2dd7-05505543.jpg",
                "uid": 566
            },
            {
                "nickname": "杨少雷",
                "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-12-22/56792a426d0b5-05505543.jpg",
                "uid": 72
            }
        ]
    }

-- end


创建班级
~~~~~~~~~~~

**URL**::

    POST      org/class/info

**POST Sample**:
.. sourcecode:: json
    {
        "organization_id":"2",
        "title":"UI设计1班",
        "class_start_date":"2015-12-12",
        "class_end_date":"2015-12-22",
        "monday":"1",
        "tuesday":"2",
        "wednesday":"3",
        "thursday":"1",
        "friday":"2",
        "saturday":"3",
        "sunday":"23"
    }

**Parameters**:

* organization_id: 机构id号
* title: 班级名称
* class_start_date: 开始上课日期，格式"2015-01-01"
* class_end_date: 结束上课日期，格式"2015-01-01"
* monday: 周一课时安排，1表示上午，2表示下午，3表示晚上，格式"123",最多3位
* tuesday: 周二课时安排
* wednesday: 周三课时安排
* thursday: 周四课时安排
* friday: 周五课时安排
* saturday: 周六课时安排
* sunday: 周日课时安排

**Response** `201` ::


    {
        "class_end_date": "2015-12-22",
        "class_start_date": "2015-12-12",
        "friday": "2",
        "id": 6,
        "monday": "1",
        "organization_id": 2,
        "saturday": "3",
        "sunday": "23",
        "thursday": "1",
        "title": "UI设计1班",
        "tuesday": "2",
        "wednesday": "3"
    }

-- end


更新班级信息
~~~~~~~~~~~

**URL**::

    PUT      org/class/info

**POST Sample**:
.. sourcecode:: json
    {
        "id":"7",
        "title":"平面设计2班",
        "class_start_date":"2015-12-10",
        "sunday":"3"
    }

**Parameters**:

* 参数均为顶部StudentClass类中的属性字段。”id”为必填字段，其余均为选填。


**Response** `202` ::


    {
        "class_end_date": "2015-12-22",
        "class_start_date": "2015-12-12",
        "friday": "2",
        "id": 6,
        "monday": "1",
        "organization_id": 2,
        "saturday": "3",
        "sunday": "23",
        "thursday": "1",
        "title": "UI设计1班",
        "tuesday": "2",
        "wednesday": "3"
    }

-- end


获取班级详细信息
~~~~~~~~~~~

**URL**::

    GET      org/class/<int:cid>/info

**Parameters**:

* cid:班级id


**Response** `200` ::


    {
        "class_end_date": "2015-12-22",
        "class_start_date": "2015-12-12",
        "friday": "2",
        "id": 6,
        "monday": "1",
        "organization_id": 2,
        "saturday": "3",
        "sunday": "23",
        "thursday": "1",
        "title": "UI设计1班",
        "tuesday": "2",
        "wednesday": "3"
    }

-- end


删除班级
~~~~~~~~~~~

**URL**::

    DELETE      org/class/<int:cid>

**Parameters**:

* cid:班级id


**Response** `202` ::


    {
        "code": 0,
        "msg": "1 class has been deleted",
        "request": "DELETE  /v1/org/class/4"
    }

-- end


将学生加入班级（支持批量加入）
~~~~~~~~~~~

**URL**::

    POST      org/class/join

**POST Sample**:
.. sourcecode:: json
    {
        "cid":"7",
        "uids":"566:567:568"
    }

**Parameters**:

* cid:班级id
* uids:学生uid,格式"uid:uid:uid"，用于批量加入

**Response** `201` ::


    {
        "code": 0,
        "msg": "3 students has been joined",
        "request": "POST  /v1/org/class/join"
    }

-- end


将学生从班级移除（支持批量移除）
~~~~~~~~~~~

**URL**::

    DELETE      org/class/quit

**POST Sample**:
.. sourcecode:: json
    {
        "cid":"7",
        "uids":"566:567:568"
    }

**Parameters**:

* cid:班级id
* uids:学生uid,格式"uid:uid:uid"，用于批量移除

**Response** `202` ::


    {
        "code": 0,
        "msg": "3 students has been removed",
        "request": "DELETE  /v1/org/class/quit"
    }

-- end