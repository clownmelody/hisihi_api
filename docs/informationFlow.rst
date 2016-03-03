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
