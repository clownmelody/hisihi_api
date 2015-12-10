.. _course:

课程
==========

获取机构课程列表
~~~~~~~~~~~~~~~
**URL**::

    GET     /<int:oid>/courses


**Parameters**:

* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

**Response** `202` ::

    {
      "courses": [
        {
          "category": {
            "allow_post": 0,
            "id": 18,
            "title": "UI设计"
          },
          "course": {
            "auth": 1,
            "category_id": 18,
            "content": "PS全集课程，让你成为PS大神",
            "id": 2,
            "img_str": "http://pic.hisihi.com/2015-12-01/565d6316e5fe9.png",
            "lecturer": 529,
            "organization_id": 2,
            "title": "PS全集课程",
            "update_time": 1449030841,
            "view_count": 36699
          },
          "lecture": {
            "nickname": "LEE",
            "sex": 0,
            "uid": 529
          }
        },
        {
          "category": {
            "allow_post": 0,
            "id": 18,
            "title": "UI设计"
          },
          "course": {
            "auth": 1,
            "category_id": 18,
            "content": "UI设计全集UI设计全集UI设计全集UI设计全集UI设计全集UI设计全集UI设计全集UI设计全集UI设计全集UI设计全集UI设计全集UI设计全集",
            "id": 3,
            "img_str": "http://pic.hisihi.com/2015-12-01/565d634fcadaa.png",
            "lecturer": 529,
            "organization_id": 2,
            "title": "UI设计全集",
            "update_time": 1449124870,
            "view_count": 36191
          },
          "lecture": {
            "nickname": "LEE",
            "sex": 0,
            "uid": 529
          }
        }
      ],
      "organization_id": 2,
      "total_count": 3
    }

