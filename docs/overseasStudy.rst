.. _overseasStudy:

留学
===========

获取banber
~~~~~~~~~~~

**URL**::

    GET      overseas_study/banner

**Parameters**:

* page: 页数，默认值为1
* per_page: 每页记录数, 默认值为20

**Response** `200` ::

    {
        "data":[
            {
                "id":18,
                "jump_type":5,
                "pic_url":"http://pic.hisihi.com/2016-04-14/570f1936bfd9e.jpg",
                "url":"hisihi://university/detailinfo?id=1"
            }
        ],
        "total_count":1
    }
-- end


获取热门国家
~~~~~~~~~~~

**URL**::

    GET      overseas_study/hot_country

**Parameters**:

* page: 页数，默认值为1
* per_page: 每页记录数, 默认值为8

**Response** `200` ::

    {
        "data":[
            {
                "id":1,
                "logo_url":"http://pic.hisihi.com/2016-05-05/572addb5c3bd9.png",
                "name":"美国"
            }
        ],
        "total_count":1
    }
-- end


获取热门大学
~~~~~~~~~~~

**URL**::

    GET      overseas_study/hot_university

**Parameters**:

* page: 页数，默认值为1
* per_page: 每页记录数, 默认值为8

**Response** `200` ::

    {
        "data":[
            {
                "id":3,
                "logo_url":"http://pic.hisihi.com/2016-05-05/572addb5c3bd9.png",
                "name":"哈弗大学"
            },
            {
                "id":1,
                "logo_url":"http://pic.hisihi.com/2016-05-05/572addb5c3bd9.png",
                "name":"斯坦福大学"
            }
        ],
        "total_count":2
    }
-- end


获取大学主页信息
~~~~~~~~~~~

**URL**::

    GET      overseas_study/university/<int:uid>

**Parameters**:

* uid: 大学ID

**Response** `200` ::

    {
        "application_requirements":"345356",
        "deadline_for_applications":"2435",
        "difficulty_of_application":"3451",
        "graduate_major":[
            "工业设计",
            "哈哈设计"
        ],
        "ielts":"3456",
        "introduction":"4365",
        "logo_url":"http://pic.hisihi.com/2016-05-05/572addb5c3bd9.png",
        "name":"哈弗大学",
        "proportion_of_undergraduates":"132",
        "scholarship":"4536",
        "school_environment":"345645",
        "share_url":"http://hisihi.com/api.php?s=/university/showuniversitymainpage/university_id/3",
        "sia_recommend_level":"34534",
        "sia_student_enrollment_rate":"234",
        "toefl":"546",
        "tuition_fees":"124",
        "undergraduate_major":[
            "平面设计",
            "XX设计"
        ],
        "web_url":"http://hisihi.com/api.php?s=/university/showuniversitymainpage/university_id/3",
        "website":"34"
    }
-- end


获取国家下大学列表
~~~~~~~~~~~

**URL**::

    GET      overseas_study/country/<int:cid>/university

**Parameters**:

* cid: 国家ID

**Response** `200` ::

    {
        "data":[
            {
                "enroll_total_count":0,
                "id":3,
                "logo_url":"http://pic.hisihi.com/2016-05-05/572addb5c3bd9.png",
                "name":"哈弗大学",
                "organization_total_count":0
            },
            {
                "enroll_total_count":0,
                "id":2,
                "logo_url":"http://pic.hisihi.com/2016-05-05/572addb5c3bd9.png",
                "name":"野鸡大学",
                "organization_total_count":0
            },
            {
                "enroll_total_count":1,
                "id":1,
                "logo_url":"http://pic.hisihi.com/2016-05-05/572addb5c3bd9.png",
                "name":"斯坦福大学",
                "organization_total_count":5
            }
        ],
        "total_count":3
    }
-- end



获取国家列表
~~~~~~~~~~~

**URL**::

    GET      overseas_study/country

**Parameters**:

* page: 页数
* per_page: 每页记录数

**Response** `200` ::

    {
        "data":[
            {
                "enroll_total_count":3,
                "id":1,
                "logo_url":"http://pic.hisihi.com/2016-05-05/572addb5c3bd9.png",
                "name":"美国",
                "university_total_count":3
            }
        ],
        "total_count":1
    }
-- end


获取大学的相册
~~~~~~~~~~~

**URL**::

    GET      overseas_study/university/<int:uid>/photos

**Parameters**:

* uid: 大学id
* page: 页数
* per_page: 每页记录数

**Response** `200` ::

    {
      "count": 3,
      "list": [
        {
          "descript": "猫243",
          "id": 3,
          "pic_url": "http://pic.hisihi.com/2016-04-11/570b23b118f31.jpg"
        },
        {
          "descript": "头像猫",
          "id": 2,
          "pic_url": "http://pic.hisihi.com/2016-04-11/570b23b118f31.jpg"
        },
        {
          "descript": "图图图图图",
          "id": 1,
          "pic_url": "http://pic.hisihi.com/2015-12-01/565d62d9c4ce4.png"
        }
      ]
    }
-- end


留学大学报名
~~~~~~~~~~~~~~~
**URL**::

    POST     /university/enroll

**Parameters**:(jsoon)

* university_id:  大学id
* uid: 用户id
* student_name: 学生姓名
* student_phone_num:  学生电话
* student_education: 学生学历
* student_qq: 学生qq(选填)]
* study_abroad_purpose: 留学目的
* apply_major: 选择专业

**Response** `201` ::

    {
      "apply_major": "室内设计",
      "create_time": 1462953005,
      "id": 1,
      "status": 1,
      "student_education": "本科",
      "student_name": "雷锅",
      "student_phone_num": "18600466074",
      "student_qq": "1173838760",
      "study_abroad_purpose": "艺术留学",
      "uid": "577",
      "university_id": "1"
    }
** end **


获取大学的专业列表
~~~~~~~~~~~
**URL**::

    GET      overseas_study/university/<int:uid>/majors

**Parameters**:

* uid: 大学id

**Response** `200` ::

    {
      "count": 4,
      "list": [
        {
          "id": 1,
          "name": "平面设计"
        },
        {
          "id": 2,
          "name": "工业设计"
        },
        {
          "id": 3,
          "name": "XX设计"
        },
        {
          "id": 4,
          "name": "哈哈设计"
        }
      ]
    }
-- end


获取所有大学列表
~~~~~~~~~~~
**URL**::

    GET      overseas_study/universities

**Parameters**:

* N/A

**Response** `200` ::

    {
        "data":[
            {
                "id":13,
                "name":"悉尼大学"
            }
        ],
        "total_count":1
    }
-- end


获取所有留学计划
~~~~~~~~~~~
**URL**::

    GET      overseas_study/org/<int:oid>/plans

**Parameters**:

* oid:  机构id

**Response** `200` ::

    {
        "data":[
            {
                "id":1,
                "url":"http://baidu.com"
            }
        ],
        "total_count":1
    }
-- end


获取留学计划详情
~~~~~~~~~~~
**URL**::

    GET      overseas_study/plans/<int:pid>

**Parameters**:

* pid:  计划id

**Response** `200` ::

    {
        "create_time":1461655721,
        "html_content":"<html>hello</html>",
        "id":1,
        "organization_id":1,
        "status":1,
        "url":"http://baidu.com"
    }
-- end


更新留学计划详情
~~~~~~~~~~~
**URL**::

    PUT      overseas_study/plans/<int:pid>

**Parameters**:

* id:  计划id
* html_content:  详情内容
* url:  计划链接

**Response** `202` ::

    {
       "create_time": 1461655721,
       "html_content": "good",
       "id": "1",
       "organization_id": 1,
       "status": 1,
       "url": "http://baidu.com"
    }
-- end


添加留学计划
~~~~~~~~~~~
**URL**::

    POST      overseas_study/plan

**Parameters**:

* oid:  机构id
* html_content:  详情内容
* url:  计划链接

**Response** `202` ::

    {
       "create_time": 1461655721,
       "html_content": "good",
       "id": "1",
       "organization_id": 1,
       "status": 1,
       "url": "http://baidu.com"
    }
-- end


删除留学计划
~~~~~~~~~~~
**URL**::

    DELETE      overseas_study/plan/<int:pid>

**Parameters**:

* pid:  留学计划id


**Response** `204` ::


-- end


请求留学计划页面
~~~~~~~~~~~
**URL**::

    POST      overseas_study/plan/index

**Parameters**:(json)

* id:  计划id
* url:  计划链接

**Response** `301` ::

    将进行一次重定向
-- end


获取留学计划网页的文本
~~~~~~~~~~~
**URL**::

    POST      overseas_study/plan/text

**Parameters**:(json)

* plans:  留学计划列表，支持返回多个计划的文本；pid为计划id, url为计划的链接
* flag:  标签，0表示预览，返回str_count个文本， 1表示编辑，返回完整html文本
* str_count:  返回的文本字数，flag=0时有效

**Example**::

    {
        "flag":"0",
        "str_count":"20",
        "plans": [
            {
                "pid":"1",
                "url":"http://pic.hisihi.com/overseas_article/2016-05-23/1464001178426599.html"
            },
            {
                "pid":"2",
                "url":"http://pic.hisihi.com/overseas_article/2016-05-25/1464155341369309.html"
            }
        ]
    }

**Response** `200` ::

    {
      "text_list": [
        {
          "pid": "1",
          "text": "shsaha ahksjdksjdk j"
        },
        {
          "pid": "2",
          "text": "shsaha ahksjdksjdk j"
        }
      ]
    }
-- end