.. _blz:

订单
===========

获取机构培训订单
~~~~~~~~~~~

**URL**::

    GET      /<int:oid>/enroll/blzs?page=:page&per_page=:per_page


**Parameters**:

* oid：机构id号
* page: 页数，默认值为1
* per_page: 每页记录数, 默认值为20

**Response** `200`:

.. sourcecode:: json

    {
      "blzs": [
        {
          "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/http://wx.qlogo.cn/mmopen/zx5ksGgvtY3iadebad7OwiaYMdvKWjqDRzzlbLDcibicPlp6F37X2J7dHibyvhYTNqpv2LI4bREHneLvzLYRGVYcFlAJToQr2RKKF/0",
          "blz": {
            "blz_id": "2345234535",
            "confirm_time": 1449471695,
            "course_id": 1,
            "create_time": 1448961237,
            "id": 4,
            "organization_id": 1,
            "phone_num": "123123123",
            "status": 2,
            "student_name": "张大海",
            "student_uid": 588,
            "student_university": "武汉科技大学"
          },
          "course": "2.1主要功能操作流程",
          "name": "李长椿"
        },
        {
          "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b11e133f0-05505543.jpg",
          "blz": {
            "blz_id": "2345234535",
            "confirm_time": null,
            "course_id": 3,
            "create_time": 1448961232,
            "id": 2,
            "organization_id": 1,
            "phone_num": "13945670987",
            "status": 1,
            "student_name": "李二狗",
            "student_uid": 565,
            "student_university": "武汉大学"
          },
          "course": "UI设计全集",
          "name": "李长春"
        },
        {
          "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b325d2dd7-05505543.jpg",
          "blz": {
            "blz_id": "234523452345",
            "confirm_time": 1449744274,
            "course_id": 77,
            "create_time": 1448961147,
            "id": 1,
            "organization_id": 1,
            "phone_num": "13876567898",
            "status": 2,
            "student_name": "赵虎",
            "student_uid": 566,
            "student_university": "武汉大学"
          },
          "course": null,
          "name": "皇帝的新衣"
        }
      ],
      "total_count": 3
    }

**Memo**:

* 查询结果将按照status状态来排序。status=1 表示待审核，status=2表示已通过, status=-2表示已拒绝


获取订单详情
~~~~~~~~~~~

**URL**::

    GET      /enroll/blz/<int:blz_id>

**Parameters**:

* blz_id: 订单号

**Response** `200` ::

  {
      "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b325d2dd7-05505543.jpg",
      "blz_id":"234523452345",
      "course_name":"UI设计",
      "create_time":1448961147,
      "status":2,
      "student_name":"赵虎",
      "uid":566
  }
** end **:


更新订单数据
~~~~~~~~~~~

**URL**::

    PUT      /enroll/blz/<int:blz_id>

**Parameters**:

* blz_id: 订单号
* status: 订单状态 2或-2

**Response** `201` ::

  {
      "status": 2
  }
** end **: