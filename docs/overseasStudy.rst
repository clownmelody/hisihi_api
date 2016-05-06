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
        "application_requirements":"这里是申请的要求",
        "deadline_for_applications":"2016年8月20日",
        "difficulty_of_application":"难",
        "graduate_major":[
            "哈哈设计"
        ],
        "ielts":"9.2",
        "introduction":"这里是学校简介",
        "logo_url":"http://pic.hisihi.com/2016-05-05/572addb5c3bd9.png",
        "name":"斯坦福大学",
        "proportion_of_undergraduates":"67%",
        "scholarship":"8000",
        "school_environment":"这里是学校环境介绍",
        "sia_recommend_level":"100&",
        "sia_student_enrollment_rate":"90%",
        "toefl":"7.0",
        "tuition_fees":"￥434，000",
        "undergraduate_major":[
            "平面设计"
        ],
        "website":"http://stf.com"
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