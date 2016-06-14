.. _forum:

论坛
==========


热门话题
~~~~~~~~~~~~~~~
**URL**::

    GET     topic/hot

**Parameters**:

* N/A

**Response** `200` ::

    {
        "data":[
            {
                "id":1,
                "title":"端午加班了吗",
                "is_hot":1,
                "description":"哈哈哈哈哈哈哈",
                "img_url":"http://pic.hisihi.com/2016-06-12/575cd088442ac.png",
                "post_count": 1
            }
        ],
        "total_count":1
    }

** end


非热门话题
~~~~~~~~~~~~~~~
**URL**::

    GET     topic/common

**Parameters**:

* page
* per_page

**Response** `200` ::

    {
        "data":[
            {
                "title":"价位阿萨德撒分",
                "img_url":"http://pic.hisihi.com/2016-06-12/575cd088442ac.png",
                "is_hot":-1,
                "description":"按时发大水发v",
                "id":2,
                "post_count": 1
            }
        ],
        "total_count":1
    }

** end


获取话题详情
~~~~~~~~~~~~~~~
**URL**::

    GET     topic/<int:tid>

**Parameters**:

* tid:   话题 id

**Response** `200` ::

    {
        "data":{
            "id":1,
            "is_hot":1,
            "img_url":"http://pic.hisihi.com/2016-06-12/575cd088442ac.png",
            "title":"端午加班了吗",
            "description":"哈哈哈哈哈哈哈",
            "post_count": 1,
            "share_web_url": "http://baidu.com"
        }
    }
