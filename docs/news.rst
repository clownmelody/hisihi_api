.. _news:

新闻
===========

获取面向机构的新闻列表
~~~~~~~~~~~~~~~~~

**URL**::

    GET      /org/news

**GET Sample**：

    http://dev.api.hisihi.com/v1/org/news?page=1&per_page=10

**Parameters**:

* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

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

**Memo**:

* 默认起始页为1


获取所属某个机构的新闻列表
~~~~~~~~~~~~~~~~~

**URL**::

    GET      /org/<int:oid>/news

**Parameters**:

* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

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

**Memo**:

* 默认起始页为1


创建机构头条
~~~~~~~~~~~~~~~
**URL**::

    POST     /org/news

**Parameters**:

* organization_id: 机构id号
* tag: 标签
* title: 标题
* content: 机构头条内容

**Response** `201` ::

    {
        "content":"hahahahah",
        "create_time":1461661752,
        "id":20,
        "tag":"test",
        "title":"ououou",
        "update_time":1461661738
    }
** end **


更新机构头条
~~~~~~~~~~~~~~~
**URL**::

    PUT     /org/news

**Parameters**:

* id: 头条id号 (必填)
* tag: 标签   （选填）
* title: 标题  （选填）
* content: 机构头条内容  （选填）

**Response** `202` ::

    {
        "content":"hahahahah",
        "create_time":1461661752,
        "id":20,
        "tag":"test",
        "title":"ououou",
        "update_time":1461661738
    }
** end **


删除机构头条
~~~~~~~~~~~~~~~
**URL**::

    DELETE     /org/news/<int:nid>

**Parameters**:

* nid: 头条id号 (必填)

**Response** `204` ::
** end **


获取机构头条信息
~~~~~~~~~~~~~~~
**URL**::

    GET     /org/news/<int:nid>

**Parameters**:

* nid: 头条id号 (必填)

**Response** `200` ::

    {
        "content":"hhhhhhh",
        "create_time":1461661752,
        "id":20,
        "tag":"test",
        "title":"ououou",
        "update_time":1461661738
    }
** end **


