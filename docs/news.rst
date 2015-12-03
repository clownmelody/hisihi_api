.. _news:

新闻
===========

获取面向机构的新闻列表
~~~~~~~~~~~~~~~~~

**URL**::

    GET      org/news

**GET Sample**：

    http://dev.api.hisihi.com/v1/org/news?page=1&per_page=10

**Parameters**:

* page：页码，默认值为1
* per_page: 每页条数，默认值为每页10条

**Response** `200`:

.. sourcecode:: json

       {
          "news": [
            {
              "content": "测试新闻",
              "create_time": 1478987653,
              "id": 1,
              "tag": "头条",
              "title": "知识就是力量",
              "update_time": 1478987653
            },
            {
              "content": "测试新闻",
              "create_time": 1478987653,
              "id": 2,
              "tag": "头条",
              "title": "知识就是力量",
              "update_time": 1478987653
            }
          ],
          "total_count": 2
        }
