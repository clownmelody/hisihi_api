.. _classmate:

班级
===========

获取指定班级学生在指定日期的签到情况
~~~~~~~~~~~

**URL**::

    GET      org/<int:oid>/class/<int:cid>/sign-in/<date>/detail

**Parameters**:

* oid: 机构id号
* cid: 班级号
* data: 日期  格式为 2015-12-11
* page: 页数，默认值为1
* per_page: 每页记录数, 默认值为20

**Response** `200` ::

    {
        "data":[
            {
                "sign_in_status":true,
                "avatar":"http://wx.qlogo.cn/mmopen/zx5ksGgvtY3iadebad7OwiaYMdvKWjqDRzzlbLDcibicPlp6F37X2J7dHibyvhYTNqpv2LI4bREHneLvzLYRGVYcFlAJToQr2RKKF/0",
                "nickname":"李长椿",
                "uid":588
            },
            {
                "sign_in_status":false,
                "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b11e133f0-05505543.jpg",
                "nickname":"李长春",
                "uid":565
            }
        ],
        "sign_in_count": 1,
        "unsign_in_count": 1,
        "total_count":2
    }
