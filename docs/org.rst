.. _org:

机构
===========
允许我偷个懒，这个类属性太多，贴段代码好了。POST、PUT参数就是属性名字。不需要传入完整属性，
需要添加、修改哪个属性就给哪个属性赋值。

.. literalinclude:: ../herovii/models/org.py

创建机构信息
~~~~~~~~~~~

**URL**::

    POST      /org

**POST Sample**：

.. sourcecode:: json

   {
       "name": "我是培训机构",
       "slogan": "培训好！",
       "logo": "img_url",
       "uid": 555,
       "type": "1#2",
       "phone_num":"18698978786",
       "city": "武汉"
    }

**Parameters**:

参数均为顶部OrgInfo类中的属性字段。出现在示例中字段信息为必填信息。
如果需要上传　** logo ** ，请先调用 :ref:`File API <file>`

不允许在创建机构信息时指定id号（不允许传入 id 这个字段），否则无法动态获取实际机构的id号



**Response** `201`:

.. sourcecode:: json

    {
        'lat': '30.498029',
        'video_img': 'video_img',
        'logo': 'logo',
        'introduce': '介绍',
        'lon': '114.421816',
        'pv': 0,
        'guarantee_num': 200,
        'slogan': '培训！培训！培训万岁',
        'name': '火星时代',
        'id': 2,
        'video': 'video',
        'location': '武汉市洪山区光谷新世界1602',
        'phone_num': '0278888888',
        'advantage': '无敌#高效'
    }


更新机构信息
~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    PUT        /org

**PUT Sample**::

    {
       "id"  : 1
       "name": "北大青鸟",
       "slogan": "培训好！"
       "logo": "img_url"
    }

**Parameters**:

参数均为顶部OrgInfo类中的属性字段。"id"为必填字段，其余均为选填。
如果需要上传　**logo** ，请先调用 :ref:`File API <file>`


查询机构信息
~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    GET      /org

**Parameters**:

* uid : 通过机构管理员id号来查找机构的基本信息
* oid : 通过机构id号来查找机构的基本信息


**Memo**:
1. 如果任何参数都不传，则会返回当前用户的机构信息
2. uid与oid为互斥参数，且oid的优先级高于uid.如果同时传递uid和oid，以oid为判断条件


获取已毕业学生
~~~~~~~~~~~~~~~
**URL**::

    GET     /<int:oid>/graduated_student

**Parameters**:

* oid: 机构id号
* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

**Response** `200` ::

    {
        "total_count":1,
        "data":[
            {
                "nickname":"13535462008",
                "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-05-14/5554bdb720f29-05505543.jpg",
                "uid":86
            }
        ]
    }
** end **


用户询问低价
~~~~~~~~~~~~~~~
**URL**::

    POST     /org/feedback/lowprice

**Parameters**:

* organization_id: 机构id号
* organization_name: 机构名称
* course_name: 课程名称
* name: 学生姓名
* phone_num: 手机号

**Response** `201` ::

    {
        "course_name":"www",
        "create_time":1461645185,
        "id":1,
        "name":"666",
        "organization_id":1,
        "organization_name":"heiwe",
        "phone_num":"12324",
        "status":1
    }
** end **


创建培训课程
~~~~~~~~~~~~~~~
**URL**::

    POST     /org/teaching_course

**Parameters**:

* organization_id: 机构id号
* course_name: 课程名称
* cover_pic: 课程图片
* start_course_time: 课程开课时间 “2015-04-12”
* lesson_period: 课时数
* student_num: 班级人数
* lecture_name: 讲师姓名
* price: 课程价格

**Response** `201` ::

    {
        "course_name":"java",
        "cover_pic":"http://sdfsaww",
        "create_time":1461655721,
        "id":1,
        "lecture_name":"rrr",
        "lesson_period":66,
        "organization_id":1001,
        "price":1000,
        "start_course_time":"2016-04-26",
        "status":1,
        "student_num":30
    }
** end **


修改培训课程
~~~~~~~~~~~~~~~
**URL**::

    PUT     /org/teaching_course

**Parameters**:

* id: 课程ID （必填）
* organization_id: 机构id号  （选填）
* course_name: 课程名称  （选填）
* cover_pic: 课程图片   （选填）
* start_course_time: 课程开课时间 “2015-04-12”  （选填）
* lesson_period: 课时数   （选填）
* student_num: 班级人数   （选填）
* lecture_name: 讲师姓名  （选填）
* price: 课程价格   （选填）

**Response** `202` ::

    {
        "course_name":"java",
        "cover_pic":"http://sdfsaww",
        "create_time":1461655721,
        "id":1,
        "lecture_name":"rrr",
        "lesson_period":66,
        "organization_id":1001,
        "price":3423,
        "start_course_time":"2016-04-26",
        "status":1,
        "student_num":30
    }
** end **


删除培训课程
~~~~~~~~~~~~~~~
**URL**::

    DELETE     /org/teaching_course/<int:cid>

**Parameters**:

* id: 课程ID （必填）

**Response** `204` ::

** end **


获取机构下培训课程列表
~~~~~~~~~~~~~~~
**URL**::

    GET     /org/<int:oid>/teaching_course

**Parameters**:

* oid: 机构ID
* page:  分页参数
* per_page:  分页参数

**Response** `200` ::

    {
        "courses":[
            {
                "already_registered":0,
                "course_name":"java",
                "cover_pic":"http://pic.hisihi.com/2015-12-01/565d62d9c4ce4.png",
                "lecture_name":"讲师2",
                "lesson_period":45,
                "organization_id":16,
                "organization_name":"刀塔天梯战队",
                "price":3423,
                "start_course_time":"2016-04-26",
                "student_num":30
            }
        ],
        "total_count":1
    }
** end **


获取培训课程信息
~~~~~~~~~~~~~~~
**URL**::

    GET     /org/teaching_course/<int:cid>

**Parameters**:

* cid: 培训课程ID

**Response** `200` ::

    {
        "already_registered":0,
        "course_name":"java",
        "cover_pic":"http://pic.hisihi.com/2015-12-01/565d62d9c4ce4.png",
        "lecture_name":"讲师2",
        "lesson_period":45,
        "organization_id":16,
        "organization_name":"刀塔天梯战队",
        "price":3423,
        "start_course_time":"2016-04-26",
        "student_num":30
    }
** end **
