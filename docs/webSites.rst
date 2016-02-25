.. _webSites:

黄页
=========

获取导航网址和分类列表
~~~~~~~~~~~~~~~~~~~~~~~
**URL**::

    GET link/yellow_pages

**Response** `200` :

    {
      "content": [
        {
          "icon_url": "werwerwqr",
          "name": "社交达人",
          "yellow_pages": [
            {
              "icon_url": "11111111",
              "url": "http://www.zhihu.com",
              "web_name": "知乎"
            },
            {
              "icon_url": "222222222",
              "url": "http://www.zhihu.com",
              "web_name": "豆瓣"
            },
            {
              "icon_url": "99999999",
              "url": "http://www.zhihu.com",
              "web_name": "FView"
            },
            {
              "icon_url": "wwwwwwwwww",
              "url": "www.baidu.com",
              "web_name": "第一个网址"
            },
            {
              "icon_url": "zhengzheng",
              "url": "wwwwwwwwwwwwwwwww",
              "web_name": "wwwwwwwwww"
            }
          ]
        },
        {
          "icon_url": "1111111",
          "name": "视频达人",
          "yellow_pages": [
            {
              "icon_url": "777777",
              "url": "http://www.zhihu.com",
              "web_name": "爱范儿"
            },
            {
              "icon_url": "8888888",
              "url": "http://www.zhihu.com",
              "web_name": "powerOn"
            }
          ]
        },
        {
          "icon_url": "wwwwwww",
          "name": "老司机",
          "yellow_pages": [
            {
              "icon_url": "3333333",
              "url": "http://www.zhihu.com",
              "web_name": "人人"
            },
            {
              "icon_url": "444444444",
              "url": "http://www.zhihu.com",
              "web_name": "微博"
            },
            {
              "icon_url": "1010101010",
              "url": "http://www.zhihu.com",
              "web_name": "贴吧"
            }
          ]
        }
      ],
      "total_count": 15
    }


获取推荐网址
~~~~~~~~~~~~~~~
**URL**::

    GET link/yellow_pages/recommend

**Response** `200` :

    [
      {
        "icon_url": "5555555",
        "url": "http://www.zhihu.com",
        "web_name": "乐乎"
      },
      {
        "icon_url": "6666666",
        "url": "http://www.zhihu.com",
        "web_name": "zealer+"
      }
    ]


创建网址信息
~~~~~~~~~~~~~

**URL**::

    POST link/yellow_page

**POST Sample**:
.. sourcecode:: json
    {
        "web_name":"豆瓣",
        "url":"www.douban.com",
        "icon_url":"http://img.taopic.com/uploads/allimg/130501/240451-13050106450911.jpg",
        "class_id":"2",
        "state":"2",
        "fake_score":3000
    }

**Parameters**:

*web_name:网址名称                  （必填）
*url:网址链接                       （必填）
*icon_url:图标地址                  （必填）
*class_id:网址类别                  （必填）
*state:网址状态（是否标识为推荐:1标识不推荐，2标识推荐，默认为1）
*real_score:真实访问量
*fake_score:后台控制访问量

**Response** `201` :

    {
      "class_id": "2",
      "fake_score": 3000,
      "icon_url": "http://img.taopic.com/uploads/allimg/130501/240451-13050106450911.jpg",
      "id": 19,
      "real_score": 0,
      "state": "2",
      "url": "www.douban.com",
      "web_name": "豆瓣"
    }


更新网址信息
~~~~~~~~~~~~~

**URL**::

    PUT link/yellow_page/<int:wid>

**PUT Sample**:
.. sourcecode:: json
    {
        "web_name":"知乎",
        "url":"www.zhihu.com",
        "icon_url":"http://img.taopic.com/uploads/allimg/130501/240451-13050106450911.jpg",
        "class_id":"1",
        "state":"1",
        "fake_score":60000,
        "status":-1
    }

**Parameters**:

*wid:网址ID
*status: 网址记录的状态，改为-1则标识删除

**Response** `202` :

    {
      "code": 0,
      "msg": " site has been updated",
      "request": "PUT  /v1/link/yellow_page/19"
    }


创建网址分类信息
~~~~~~~~~~~~~~~~~

**URL**::

    POST link/category

**POST Sample**:
.. sourcecode:: json
    {
        "category_name":"社交网络",
        "icon_url":"http://img.taopic.com/uploads/allimg/130501/240451-13050106450911.jpg"
    }

**Parameters**:

*category_name:分类名称             （必填）
*icon_url:图标地址                  （必填）

**Response** `201` :

    {
      "category_name": "社交网络",
      "icon_url": "http://img.taopic.com/uploads/allimg/130501/240451-13050106450911.jpg",
      "id": 9
    }


更新网址分类信息
~~~~~~~~~~~~~~~~~~~

**URL**::

    PUT link/category/<int:cid>

**PUT Sample**:
.. sourcecode:: json
    {
        "status":-1
    }

**Parameters**:

*cid:网址类型ID
*status: 网址分类记录的状态，改为-1则标识删除

**Response** `202` :

    {
      "code": 0,
      "msg": " category has been updated",
      "request": "PUT  /v1/link/category/9"
    }