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
            "info":{
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
                "supportCount":1808,
                "title":"精益求精,彰显微小细节的5件设计",
                "update_time":1456107041,
                "view":62658
            }
        },
        {
            "content_type":2,
            "id":12,
            "info":{
                "ViewCount":36377,
                "duration":235,
                "id":46,
                "img":"http://pic.hisihi.com/2016-02-29/1456726581454771.jpg",
                "lecturer":103,
                "lecturer_name":"皮卡Q",
                "organization_logo":"http://pic.hisihi.com/2016-02-29/1456727795774772.jpg@13-13-355-355a",
                "title":"钢铁侠教你如何制杖",
                "type":"平面设计"
            }
        },
        {
            "content_type":3,
            "id":11,
            "info":{
                "content_url":"http://tencent.com",
                "pic":"http://advs-pic.oss-cn-qingdao.aliyuncs.com/2015-12-07/5665064bcfefa.png",
                "size":[
                    560,
                    347
                ],
                "title":"广告-02",
                "type":"advertisment"
            }
        }
    ],
    "total_count":3
}