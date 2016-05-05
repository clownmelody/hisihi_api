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