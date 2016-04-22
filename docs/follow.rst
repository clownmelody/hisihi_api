.. _follow:

推荐的人
=========

获取推荐的人列表
~~~~~~~~~~~~~~~~~~~~~~~
**URL**::

    GET follow/recommend_users

**Response** `200` ::

    {
        "count":5,
        "recommend_id":"72,560,595,596,597,598,601",
        "users":[
            {
                "nickname":"我就是我",
                "path":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-25/56559b8e52d14-05505543.jpg",
                "type":"alumni",
                "uid":560
            },
            {
                "nickname":"Leslie",
                "path":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-12-22/56792a426d0b5-05505543.jpg",
                "type":"alumni",
                "uid":72
            },
            {
                "nickname":"天涯浪子ou",
                "path":"http://tp3.sinaimg.cn/1750080094/180/5621520514/1",
                "type":"recommend",
                "uid":595
            },
            {
                "nickname":"落羽",
                "path":"http://q.qlogo.cn/qqapp/1104475505/3B7FEBFC518D235C944FF863C4B92BA5/100",
                "type":"recommend",
                "uid":596
            },
            {
                "nickname":"Jimmy",
                "path":"http://wx.qlogo.cn/mmopen/zx5ksGgvtY3iadebad7OwiaflDyaQqiaJXQiaGYpnUNZJoR1eupHUOMpgCJe9cA0Nr1OT018icRHYXf0bNp1kMB6tlA3uJa92RLjQ/0",
                "type":"recommend",
                "uid":597
            }
        ]
    }

关注推荐的人
~~~~~~~~~~~~~~~
**URL**::

    POST follow/follow_user

**POST Sample**：

.. sourcecode:: json

    {
        "uid" : "72",
        "recommend_id" : "72,560,595,596,597,598,601",
        "recommend_type" : "alumni"
    }

**Parameters**:

* uid: 被关注人的ID
* recommend_id: 由客户端取当前推荐列表里的uid拼成字符串
* recommend_type: 推荐列表返回的用户信息中的type值

**Response** `201` ::

    {
        "info":"关注成功",
        "user":{
            "nickname":"龙儿。",
            "path":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-07-15/55a5ffd09451b-05505543.jpg",
            "type":"alumni",
            "uid":165
        }
    }
    如果已经关注过了，则返回：
    {
      "info": "您已经关注过了",
      "user": null
    }
    如果已经没有可推荐的校友，则返回：
    {
        "info": "关注成功",
        "user": null
    }
