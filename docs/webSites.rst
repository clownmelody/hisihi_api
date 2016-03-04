.. _webSites:

黄页
=========

获取黄页分类列表
~~~~~~~~~~~~~~~~~~~~~~~
**URL**::

    GET link/yellow_pages

**Response** `200` :

.. sourcecode:: json
    {
        "data":
        [
            {
                "category_icon": "http://pic.hisihi.com/2016-03-03/56d80e46681f8.png",
                "category_name": "网址大全",
                "count": 5,
                "data":
                [
                    {
                        "icon": null,
                        "site_logo": null,
                        "site_name": "powerOn",
                        "site_url": "http://www.zhihu.com"
                    },
                    {
                        "icon": null,
                        "site_logo": null,
                        "site_name": "FView",
                        "site_url": "http://www.zhihu.com"
                    },
                    {
                        "icon": null,
                        "site_logo": null,
                        "site_name": "贴吧",
                        "site_url": "http://www.zhihu.com"
                    },
                    {
                        "icon": "http://pic.hisihi.com/2016-03-04/56d92174e3b6b.png",
                        "site_logo": "http://pic.hisihi.com/2016-03-03/56d81586d02f2.png",
                        "site_name": "json",
                        "site_url": "http://json.cn/"
                    },
                    {
                        "icon": "http://pic.hisihi.com/2016-03-04/56d922a72fd5e.png",
                        "site_logo": "http://pic.hisihi.com/2016-03-03/56d80e46681f8.png",
                        "site_name": "hao123",
                        "site_url": "http://www.hao123.com/"
                    }
                ]
            }
        ],
        "total_count": 2
    }




获取首页推荐网址
~~~~~~~~~~~~~~~
**URL**::

    GET link/yellow_pages/recommend

**Response** `200` :

.. sourcecode:: json
    {
        "data":
        [
            {
                "icon": "http://pic.hisihi.com/2016-03-04/56d922a72fd5e.png",
                "site_logo": "http://pic.hisihi.com/2016-03-04/56d92d8e04225.png",
                "site_name": "知乎",
                "site_url": "http://www.zhihu.com"
            },
            {
                "icon": null,
                "site_logo": "",
                "site_name": "豆瓣",
                "site_url": "http://www.zhihu.com"
            },
            {
                "icon": "http://pic.hisihi.com/2016-03-04/56d92174e3b6b.png",
                "site_logo": "http://pic.hisihi.com/2016-03-03/56d81586d02f2.png",
                "site_name": "json",
                "site_url": "http://json.cn/"
            },
            {
                "icon": "http://pic.hisihi.com/2016-03-04/56d922a72fd5e.png",
                "site_logo": "http://pic.hisihi.com/2016-03-03/56d80e46681f8.png",
                "site_name": "hao123",
                "site_url": "http://www.hao123.com/"
            }
        ],
        "total_count": 4
    }


