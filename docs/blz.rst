.. _blz:

订单
===========

获取机构培训订单
~~~~~~~~~~~

**URL**::

    GET      /<int:oid>/enroll/blzs


**Parameters**:

* oid：机构id号

**Response** `200`:

.. sourcecode:: json

    [
      {
        "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b11e133f0-05505543.jpg",
        "blz": {
          "blz_id": "2345234535",
          "confirm_time": null,
          "course_id": 3,
          "id": 2,
          "organization_id": 2,
          "phone_num": "13945670987",
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
          "confirm_time": null,
          "course_id": 2,
          "id": 1,
          "organization_id": 2,
          "phone_num": "13876567898",
          "student_name": "赵虎",
          "student_uid": 566,
          "student_university": "武汉大学"
        },
        "course": "PS全集课程",
        "name": "皇帝的新衣"
      }
    ]