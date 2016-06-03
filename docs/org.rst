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

机构类型为留学type=31时，可传入参数 university_id，格式1:2:3，关联所选大学

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

机构类型为留学type=31时，可传入参数 university_id，格式1:2:3，关联所选大学

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

**Response** `200` ::

    {
        "advantage":"上市大公司#明星讲师#环境相当优越#设备非常先进#早晚班车接送#午餐供应#过节大礼包",
        "city":"武汉",
        "guarantee_num":200,
        "id":16,
        "introduce":"今天天气真好啊！",
        "latitude":null,
        "location":"洪山区野芷湖一号89037489347983742128号",
        "logo":"http://pic.hisihi.com/2015-12-07/56654dfc5df6a.JPG",
        "longitude":null,
        "name":"刀塔天梯战队",
        "phone_num":"123123123",
        "slogan":"学设计就上嘿设汇",
        "type":30,
        "video":"",
        "video_img":"",
        "view_count":1968
    }

    备注：type： 14-手绘 15-留学 16-软件 （生产环境）; 30-软件 31-留学 32-手绘 （测试环境）;
** end **

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
* university_id:  大学id
* course_name: 课程名称
* cover_pic: 课程图片
* start_course_time: 课程开课时间 “2015-04-12”
* end_course_time: 课程结束时间
* lesson_period: 课时数
* student_num: 班级人数
* lecture_name: 讲师姓名
* price: 课程价格
* introduction: 介绍
* plan: 计划

**Response** `201` ::

    {
        "already_registered":0,
        "course_name":"ps",
        "cover_pic":"http://123",
        "create_time":1463464226,
        "id":7,
        "introduction":"intrio",
        "lecture_name":"test",
        "lesson_period":3,
        "organization_id":41,
        "plan":"123",
        "price":1000,
        "start_course_time":"2016-06-09",
        "end_course_time":"2016-04-26",
        "status":1,
        "student_num":3
    }
** end **


修改培训课程
~~~~~~~~~~~~~~~
**URL**::

    PUT     /org/teaching_course

**Parameters**:

* id: 课程ID （必填）
* organization_id: 机构id号  （选填）
* university_id:  大学id （选填）
* course_name: 课程名称  （选填）
* cover_pic: 课程图片   （选填）
* start_course_time: 课程开课时间 “2015-04-12”  （选填）
* end_course_time: 课程结束时间 “2015-04-12”  （选填）
* lesson_period: 课时数   （选填）
* student_num: 班级人数   （选填）
* lecture_name: 讲师姓名  （选填）
* price: 课程价格   （选填）
* introduction: 介绍 （选填）
* plan: 计划  （选填）

**Response** `202` ::

    {
        "already_registered":0,
        "course_name":"ps",
        "cover_pic":"http://123",
        "create_time":1463464226,
        "id":7,
        "introduction":"intrio",
        "lecture_name":"test",
        "lesson_period":3,
        "organization_id":41,
        "plan":"123",
        "price":1000,
        "start_course_time":"2016-06-09",
        "end_course_time":"2016-06-09",
        "status":1,
        "student_num":3
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
* except_id: 排除的课程ID（传参方式同分页参数, 用于课程）
* page:  分页参数
* per_page:  分页参数

**Response** `200` ::

    {
        "courses":[
            {
                "already_registered":0,
                "course_name":"PS-01",
                "cover_pic":"http://pic.hisihi.com/2015-12-01/565d62d9c4ce4.png",
                "end_course_time":"",
                "id":3,
                "lecture_name":"讲师3",
                "lesson_period":31,
                "organization_id":41,
                "organization_name":"英雄联盟开黑组",
                "price":2000,
                "start_course_time":"2016-05-01",
                "student_num":30
            }
        ],
        "total_count":1
    }
** end **


获取机构下培训课程列表(v2.9)
~~~~~~~~~~~~~~~
**URL**::

    GET     /org/<int:oid>/teaching_course

**Parameters**:

* version 2.9
* oid: 机构ID
* except_id: 排除的课程ID（传参方式同分页参数, 用于课程）
* page:  分页参数
* per_page:  分页参数

**Response** `200` ::

    {
      "courses": [
        {
          "already_registered": 0,
          "coupon_list": [
            {
              "coupon_info": {
                "end_time": 1464624000,
                "id": 1,
                "is_obtain": true,
                "is_out_of_date": false,
                "is_used": false,
                "money": 200,
                "name": "直减200",
                "obtain_id": 6,
                "start_time": 1464105600,
                "type": 1
              },
              "promotion_info": {
                "description": "嘿设汇亿元机构扶持计划ppppp",
                "id": 1,
                "little_logo_url": "http://pic.hisihi.com/2016-05-23/574287226672b.png",
                "logo_url": "http://pic.hisihi.com/2016-05-23/57429b5d4d4f6.png",
                "tag_url": "http://pic.hisihi.com/2016-05-23/574287226672b.png",
                "title": "亿元扶持1",
                "type": 1
              }
            }
          ],
          "course_name": "PS-01",
          "cover_pic": "http://pic.hisihi.com/2015-12-01/565d62d9c4ce4.png",
          "end_course_time": "",
          "id": 3,
          "lecture_name": "讲师3",
          "lesson_period": 31,
          "organization_id": 41,
          "organization_name": "英雄联盟开黑组",
          "price": 2000,
          "start_course_time": "2016-05-01",
          "student_num": 30
        },
        {
          "already_registered": 0,
          "coupon_list": [],
          "course_name": "nodejs全栈式开发",
          "cover_pic": "http://pic.hisihi.com/2016-05-17/1463467535627281.jpg",
          "end_course_time": "2015-09-08",
          "id": 8,
          "lecture_name": "MR.JJM",
          "lesson_period": 120,
          "organization_id": 41,
          "organization_name": "英雄联盟开黑组",
          "price": 16888,
          "start_course_time": "2016-06-08",
          "student_num": 30
        }
      ],
      "total_count": 10
    }

    当is_obtain=true时，返回obtain_id，用于获取领取的优惠券详情
** end **


获取培训课程信息
~~~~~~~~~~~~~~~
**URL**::

    GET     /org/teaching_course/<int:cid>

**Parameters**:

* cid: 培训课程ID

**Response** `200` ::

    {
        "course_name":"UI",
        "cover_pic":"http://pic.hisihi.com/2015-12-01/565d62d9c4ce4.png",
        "end_course_time":"",
        "lecture_name":"讲师1",
        "lesson_period":23,
        "organization_id":60,
        "organization_name":"北京测试机构",
        "price":1200,
        "start_course_time":"2016-04-27",
        "student_num":40,
        "web_url":"http://hisihi.com/api.php?s=/organization/showteachingcoursemainpage/course_id/2"
    }
** end **


获取培训课程详情
~~~~~~~~~~~~~~~
**URL**::

    GET     /org/teaching_course/<int:cid>/detail

**Parameters**:

* cid: 培训课程ID

**Response** `200` ::

    {
        "already_registered":0,
        "course_name":"UI",
        "cover_pic":"http://pic.hisihi.com/2015-12-01/565d62d9c4ce4.png",
        "end_course_time":"",
        "enroll_info":{
            "data":[
                {
                    "create_time":1462508625,
                    "nickname":"mnbv1234",
                    "student_phone_num":"13100002324",
                    "uid":74
                },
                {
                    "avatar":"http://q.qlogo.cn/qqapp/1104475505/6B7F2330FA95A5DD7AF1DF2E0EB77915/100",
                    "create_time":1462772925,
                    "nickname":"多多",
                    "student_phone_num":"15872386222",
                    "uid":602
                }
            ],
            "total_count":2
        },
        "introduction":"介绍2",
        "lecture_name":"讲师1",
        "lesson_period":23,
        "light_authentication":1,
        "organization_id":60,
        "organization_name":"北京测试机构",
        "plan":"安排2",
        "price":1200,
        "start_course_time":"2016-04-27",
        "student_num":40
    }
** end **


获取培训课程报名信息
~~~~~~~~~~~~~~~
**URL**::

    GET     /teaching_course/<int:cid>/enroll

**Parameters**:

* cid: 培训课程ID
* page:  分页参数
* per_page:  分页参数

**Response** `200` ::

     {
        "data":[
            {
                "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-12-22/56792a426d0b5-05505543.jpg",
                "create_time":1450777736,
                "nickname":"Leslie",
                "student_phone_num":"123",
                "uid":72
            }
        ],
        "total_count":1
     }
** end **


用户培训课程报名
~~~~~~~~~~~~~~~
**URL**::

    POST     /teaching_course/<int:cid>/enroll

**Parameters**:

* course_id:  课程id
* uid: 用户id
* student_name: 学生姓名
* student_phone_num:  学生电话
* student_university: 学生大学
* student_qq: 学生qq(选填)

**Response** `201` ::

    {
        "course_id":2,
        "create_time":1462362166,
        "id":3,
        "status":1,
        "student_name":"653",
        "student_phone_num":"13100002324",
        "student_qq":null,
        "student_university":"pku",
        "student_qq": "213423",
        "uid":74
    }
** end **


机构添加专业
~~~~~~~~~~~~~~~
**URL**::

    POST     /major

**Parameters**:(json)

* oid:  机构id
* major_id: 专业id,格式36:35:33

**Response** `201` ::

    {
      "code": 0,
      "msg": "2 major has been added",
      "request": "POST  /v1/org/major"
    }
** end **


获取机构的专业
~~~~~~~~~~~~~~~
**URL**::

    GET     /major/<int:oid>

**Parameters**:

* oid:  机构id

**Response** `200` ::

    {
      "organization_id": 60,
      "major_list": [
        {
          "id": 35,
          "value": "网页"
        },
        {
          "id": 36,
          "value": "插画"
        }
      ]
    }
** end **


获取所有机构专业列表
~~~~~~~~~~~~~~~
**URL**::

    GET     /tag/<int:tag_type>

**Parameters**:

* tag_type:  标签类型id，专业标签固定值tag_type=8

**Response** `200` ::

    [
      {
        "create_time": 1462330462,
        "extra": "http://pic.hisihi.com/2016-05-04/5729645a0db1d.png",
        "id": 33,
        "type": 8,
        "value": "UI"
      },
      {
        "create_time": 1462330486,
        "extra": "http://pic.hisihi.com/2016-05-04/57296473b07cf.png",
        "id": 34,
        "type": 8,
        "value": "平面"
      },
      {
        "create_time": 1462330513,
        "extra": "http://pic.hisihi.com/2016-05-04/5729648ebea5d.png",
        "id": 35,
        "type": 8,
        "value": "网页"
      },
      {
        "create_time": 1462330530,
        "extra": "http://pic.hisihi.com/2016-05-04/572964a030841.png",
        "id": 36,
        "type": 8,
        "value": "插画"
      }
    ]
** end **


获取机构的简要信息（课程下的机构展示信息）
~~~~~~~~~~~~~~~
**URL**::

    GET     /<int:oid>/base

**Parameters**:

* oid:  机构id

**Response** `200` ::

    {
        "logo":"http://pic.hisihi.com/2015-12-01/565d633e3d4ed.png",
        "view_count":2498,
        "follow_count":8,
        "auth":[
            {
                "default_display":0,
                "tag_pic_url":"",
                "pic_url":"http://pic.hisihi.com/2015-12-02/565e6ba9add2f.png",
                "content":"嘿设汇为在线报名支付信用担保",
                "disable_pic_url":"",
                "status":true,
                "name":"支付担保",
                "id":2
            },
            {
                "default_display":0,
                "tag_pic_url":"",
                "pic_url":"http://pic.hisihi.com/2015-12-02/565e6dcd5f74f.png",
                "content":"嘿设汇为机构信誉担保",
                "disable_pic_url":"",
                "status":false,
                "name":"信誉担保",
                "id":3
            },
            {
                "default_display":1,
                "tag_pic_url":"http://pic.hisihi.com/2015-12-02/565ed4ef4f60e.png",
                "pic_url":"http://pic.hisihi.com/2015-12-03/565faef8618b4.png",
                "content":"嘿设汇进行评估认证",
                "disable_pic_url":"http://pic.hisihi.com/2015-12-03/565faf03f2270.png",
                "status":false,
                "name":"嘿设汇认证",
                "id":4
            },
            {
                "default_display":1,
                "tag_pic_url":"http://pic.hisihi.com/2015-12-02/565ed4fa22906.png",
                "pic_url":"http://pic.hisihi.com/2015-12-03/565fb1c61bd54.png",
                "content":"诚信机构诚信机构诚信机构诚信机构诚信机构诚信机构诚信机构诚信机构诚信机构诚信机构诚信机构诚信机构",
                "disable_pic_url":"http://pic.hisihi.com/2015-12-03/565fb1cd92b81.png",
                "status":false,
                "name":"诚信机构",
                "id":8
            }
        ],
        "name":"黑马绘画培训机构",
        "enroll_count":14,
        "id":2
    }
** end **


获取机构已绑定的大学
~~~~~~~~~~~~~~~
**URL**::

    GET     /<int:oid>/university

**Parameters**:

* oid:  机构id

**Response** `200` ::

    {
      "university_list": [
        {
          "id": 1,
          "name": "斯坦福大学"
        }
      ],
      "organization_id": 41
    }
** end **


机构添加大学
~~~~~~~~~~~~~~~
**URL**::

    POST     /org/link/university

**Parameters**:(json)

* oid:  机构id
* university_id: 大学id,格式36:35:33

**Response** `201` ::

    {
      "code": 0,
      "msg": "3 university has been added",
      "request": "POST  /v1/org/link/university"
    }
** end **


获取活动详情
~~~~~~~~~~~~~~~
**URL**::

    GET     /org/promotion/<int:pid>

**Parameters**:

* pid:  活动id

**Response** `200` ::

    {
        "title":"亿元扶持1",
        "id":1,
        "tag_url":"http://pic.hisihi.com/2016-05-23/574287226672b.png",
        "little_logo_url":"http://pic.hisihi.com/2016-05-23/574287226672b.png",
        "type":1,
        "logo_url":"http://pic.hisihi.com/2016-05-23/57429b5d4d4f6.png",
        "description":"嘿设汇亿元机构扶持计划ppppp",
        "detail_web_url": "http://baidu.com"
    }
** end **


获取活动相关的课程列表
~~~~~~~~~~~~~~~
**URL**::

    GET     /org/promotion/<int:pid>/teaching_course

**Parameters**:

* pid:  活动id

**Response** `200` ::

    {
        "total_count":2,
        "data":[
            {
                "student_num":46,
                "end_course_time":"",
                "lesson_period":34,
                "cover_pic":"http://pic.hisihi.com/2015-12-01/565d62d9c4ce4.png",
                "organization_name":"河北测试机构",
                "start_course_time":"2016-04-27",
                "organization_id":62,
                "coupon_info":{
                    "type":1,
                    "end_time":1464624000,
                    "name":"直减200",
                    "is_obtain":false,
                    "money":200,
                    "id":1,
                    "is_used":false,
                    "start_time":1464105600,
                    "is_out_of_date":false
                },
                "course_name":"UI-01",
                "web_url":"http://hisihi.com/api.php?s=/organization/showteachingcoursemainpage/course_id/23",
                "price":2200,
                "lecture_name":"讲师01"
            },
            {
                "student_num":43,
                "end_course_time":"",
                "lesson_period":25,
                "cover_pic":"http://pic.hisihi.com/2015-12-01/565d62d9c4ce4.png",
                "organization_name":"河北测试机构",
                "start_course_time":"2016-04-27",
                "organization_id":62,
                "coupon_info":{
                    "type":1,
                    "end_time":1464624000,
                    "name":"直减200",
                    "is_obtain":false,
                    "money":200,
                    "id":1,
                    "is_used":false,
                    "start_time":1464105600,
                    "is_out_of_date":false
                },
                "course_name":"UI-03",
                "web_url":"http://hisihi.com/api.php?s=/organization/showteachingcoursemainpage/course_id/24",
                "price":1100,
                "lecture_name":"讲师02"
            }
        ]
    }
** end **


课程主页获取活动和优惠券列表
~~~~~~~~~~~~~~~
**URL**::

    GET     /org/teaching_course/<int:cid>/promotions

**Parameters**:

* cid:  课程id

**Response** `200` ::

    {
        "data":[
            {
                "coupon_info":{
                    "end_time":1464624000,
                    "id":1,
                    "is_obtain":false,
                    "is_out_of_date":false,
                    "is_used":false,
                    "money":200,
                    "name":"直减200",
                    "start_time":1464105600,
                    "type":1
                },
                "promotion_info":{
                    "description":"嘿设汇亿元机构扶持计划ppppp",
                    "id":1,
                    "little_logo_url":"http://pic.hisihi.com/2016-05-23/574287226672b.png",
                    "logo_url":"http://pic.hisihi.com/2016-05-23/57429b5d4d4f6.png",
                    "tag_url":"http://pic.hisihi.com/2016-05-23/574287226672b.png",
                    "title":"亿元扶持1",
                    "type":1
                }
            }
        ],
        "total_count":1
    }
** end **