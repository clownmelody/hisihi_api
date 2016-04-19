.. _informationFlow:

首页信息流
==========

banner列表
~~~~~~~~~~~~~~~
**URL**::

     GET    information_flow/banner

**Parameters**:

* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

**Response** `200` ::

    {
        "data":[
            {
                "id":1,
                "pic_url":"http://pic.hisihi.com/2016-03-03/56d7dc2b4cd14.png",
                "url":"http://www.baidu.com/hahah"
            },
            {
                "id":2,
                "pic_url":"http://pic.hisihi.com/2016-03-03/56d7d67d2a3c1.png",
                "url":"http://www.baidu.com/"
            }
        ],
        "total_count":2
    }
--

banner列表（version-2.7）
~~~~~~~~~~~~~~~
**URL**::

     GET    information_flow/banner

**Parameters**:

* version  版本号
* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

**Response** `200` ::

    {
        "data":[
            {
                "id":15,
                "jump_type":1,
                "pic_url":"http://pic.hisihi.com/2016-04-05/5703669815157.png",
                "url":"http://www.runoob.com"
            }
        ],
        "total_count":1
    }
--

混排内容列表
~~~~~~~~~~~~~~~
**URL**::

     GET    information_flow/content

**Parameters**:

* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条
* type:  内容类型

**Response** `200` ::

    {
    "data":[
        {
            "content_type":1,
            "id":14,
            "top_content_info":{
                "content_url":"http://hisihi.com/app.php/public/topcontent/version/2.0/type/view/id/1768",
                "create_time":1455605640,
                "description":"",
                "id":1768,
                "img":"http://forum-pic.oss-cn-qingdao.aliyuncs.com/2016-02-16/56c2c77d908be.jpg",
                "isFavorited":false,
                "isSupportd":false,
                "logo_pic":"http://hisihi-other.oss-cn-qingdao.aliyuncs.com/2016-02-16/56c2c78ba212c.jpg",
                "share_url":"http://hisihi.com/app.php/public/v2contentforshare/type/view/version/2.3/id/1768",
                "source_name":"嘿设汇",
                "supportCount":1891,
                "title":"精益求精,彰显微小细节的5件设计",
                "update_time":1456107041,
                "view":62658
            }
        },
        {
            "content_type":2,
            "course_info":{
                "ViewCount":41137,
                "duration":235,
                "id":46,
                "img":"http://pic.hisihi.com/2016-02-29/1456726581454771.jpg",
                "lecturer":103,
                "lecturer_name":"皮卡Q",
                "organization_logo":"http://pic.hisihi.com/2016-02-29/1456727795774772.jpg@13-13-355-355a",
                "title":"钢铁侠教你如何制杖",
                "type":"平面设计"
            },
            "id":12
        },
        {
            "adv_info":{
                "content_url":"http://tencent.com",
                "pic":"http://advs-pic.oss-cn-qingdao.aliyuncs.com/2015-12-07/5665064bcfefa.png",
                "size":[
                    560,
                    347
                ],
                "title":"广告-02",
                "type":"advertisment"
            },
            "content_type":3,
            "id":11
        }
    ],
    "total_count":3
}


混排内容列表(version-2.7)
~~~~~~~~~~~~~~~
**URL**::

     GET    information_flow/content

**Parameters**:

* version  版本号
* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条
* type:  内容类型

**Response** `200` ::

    {
    "data":[
        {
            "content_type":1,
            "id":14,
            "top_content_info":{
                "content_url":"http://hisihi.com/app.php/public/topcontent/version/2.0/type/view/id/1768",
                "create_time":1455605640,
                "description":"",
                "id":1768,
                "cover_type":2,
                "img":"http://forum-pic.oss-cn-qingdao.aliyuncs.com/2016-02-16/56c2c77d908be.jpg",
                "isFavorited":false,
                "isSupportd":false,
                "logo_pic":"http://hisihi-other.oss-cn-qingdao.aliyuncs.com/2016-02-16/56c2c78ba212c.jpg",
                "share_url":"http://hisihi.com/app.php/public/v2contentforshare/type/view/version/2.3/id/1768",
                "source_name":"嘿设汇",
                "supportCount":1891,
                "title":"精益求精,彰显微小细节的5件设计",
                "update_time":1456107041,
                "view":62658
            }
        },
        {
            "adv_info":{
                "content_url":"http://tencent.com",
                "pic":"http://advs-pic.oss-cn-qingdao.aliyuncs.com/2015-12-07/5665064bcfefa.png",
                "size":[
                    560,
                    347
                ],
                "title":"广告-02",
                "type":"advertisment"
            },
            "content_type":3,
            "id":11
        }
    ],
    "total_count":2
}


配置类型列表
~~~~~~~~~~~~~~~
**URL**::

     GET    information_flow/type
**Response** `200` ::

    {
        "data":[
            {
                "id":1,
                "title":"平面"
            }
        ],
        "total_count":1
    }


首页搜索列表
~~~~~~~~~~~~~~~
**URL**::

     GET    information_flow/search

**Parameters**:

* keywords  关键字


**Response** `200` ::

    {
    "data":[
        {
            "content_type":1,
            "id":1260,
            "top_content_info":{
                "content_url":"http://hisihi.com/app.php/public/topcontent/version/2.0/type/view/id/1260",
                "cover_type":1,
                "create_time":1434726420,
                "description":"",
                "id":1260,
                "img":"http://forum-pic.oss-cn-qingdao.aliyuncs.com/2015-06-19/5584302697419.jpg",
                "isFavorited":false,
                "isSupportd":false,
                "logo_pic":null,
                "share_url":"http://hisihi.com/app.php/public/v2contentforshare/type/view/version/2.3/id/1260",
                "source_name":"",
                "supportCount":11999,
                "title":"请原谅你的设计师男友",
                "update_time":1435629865,
                "view":114983
            }
        },
        {
            "content_type":1,
            "id":1261,
            "top_content_info":{
                "content_url":"http://hisihi.com/app.php/public/topcontent/version/2.0/type/view/id/1261",
                "cover_type":2,
                "create_time":1434726840,
                "description":"",
                "id":1261,
                "img":"http://forum-pic.oss-cn-qingdao.aliyuncs.com/2016-04-14/570f1936bfd9e.jpg",
                "isFavorited":false,
                "isSupportd":false,
                "logo_pic":"http://hisihi-other.oss-cn-qingdao.aliyuncs.com/2016-04-14/570f1936bfd9e.jpg",
                "share_url":"http://hisihi.com/app.php/public/v2contentforshare/type/view/version/2.3/id/1261",
                "source_name":"heheh",
                "supportCount":12287,
                "title":"北京服装学院艺术设计学院 2015毕业设计",
                "update_time":1460965528,
                "view":117782
            }
        }
    ],
    "total_count":2
}


--