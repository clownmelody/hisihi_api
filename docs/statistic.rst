.. _statistic:

统计
==========

活动的PV量加1次
~~~~~~~~~~~~~~~
URL::

    PUT     /online/pv+1

PUT::

    {
        "oid": 4
    }

Parameters:

* oid: 需要增加pv的活动的id号

Response Status `202` ::

    {
        "code": 0,
        "msg": "ok",
        "request": "PUT  /v1/online/pv+1"
    }


活动的分享次数+1
~~~~~~~~~~~~~~~
URL::

    PUT     /online/share+1

PUT::

    {
        "oid": 4
    }

Parameters:

* oid: 需要增加分享次数的活动的id号

Response Status `202` ::

    {
        "code": 0,
        "msg": "ok",
        "request": "PUT  /v1/pk/share+1"
    }


安装包的下载数量+1
~~~~~~~~~~~~~~~~~~~~
URL::

    PUT       /pk/download+1

PUT::

    {
        "oid" : 4
        "channel" : 1
    }

Parameters:

* channel: 1 表示通过online活动的方式下载了一次安装包，可取值 [1 | "1" | "online"]
* oid: 当channel="online"时，表示活动的id号

Response Status `202` ::

    {
        "code": 0,
        "msg": "ok",
        "request": "PUT  /v1/pk/download+1"
    }


机构学生报名情况统计
~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    GET     /org/<int:oid>/student/enroll/stats/count


**Parameters**:

* oid: 机构的id号 （必填）


Response Status `200` :

.. sourcecode:: json

    {
        "in_count": 25
        "standby_count": 3
    }

**Memo**:

* in_count, 现有学生数(已报名)
* standby_count, 待处理的人数


机构学生签到情况统计
~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    GET     /org/<int:oid>/student/sign-in/stats/count


**GET Sample**:

    http://dev.api.hisihi.com/v1/org/2/student/sign-in/stats/count?page=1&per_page=10

**Parameters**:

* oid: 机构的id号 （必选）
* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条
* since: 查询起始时间的时间戳（秒）
* end: 查询截止时间的时间戳 （秒）

**Response** `200` :

.. sourcecode:: json

      {
          "record_total_count": 6,
          "sign_in_stats": [
            {
              "date": "2015-12-09",
              "sign_in_count": 1,
              "total_count": 4
            },
            {
              "date": "2015-12-08",
              "sign_in_count": 1,
              "total_count": 4
            },
            {
              "date": "2015-12-07",
              "sign_in_count": 1,
              "total_count": 0
            }
          ]
        }

**Memo**:

* 返回json数据按时间倒叙排列
* sign_in_count, 某日签到人数
* total_count, 某日机构总人数
* 注意: 如果某日没有学生打开，则这天的数据统计不会出现在返回数据中。对客户端的影响在于，最新一天的统计情况极有可能不会出现
  在返回结果中。这就意味着今天签到的人数为0。如果需要获取总人数，可以使用前一天的人数作为总人数。


机构学生单天签到情况统计
~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    GET     /org/<int:oid>/student/sign-in/<date>/stats/count

**GET Sample**:

    http://dev.api.hisihi.com/v1/org/2/student/sign-in/2015-12-08/stats/count

**Parameters**:

* oid: 机构的id号 （必选）
* date: 需要查询的日期，如'2015-12-08'.注意，月和日如果不足两位数必须使用‘0’来补位。'2015-3-8'这样的日期
        一定不会查询到结果

**Response** `200` :

.. sourcecode:: json
    {
      "date": "2015-12-09",
      "sign_in_count": 1,
      "total_count": 4
    }


机构所有班级单天的签到情况
~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    GET     /org/<int:oid>/class/sign-in/<date>/stats/count

**GET Sample**:

    http://dev.api.hisihi.com/v1/org/2/class/sign-in/2015-12-08/stats/count

**Parameters**:

* oid: 机构的id号 （必选）
* date: 需要查询的日期，如'2015-12-08'.注意，月和日如果不足两位数必须使用‘0’来补位。'2015-3-8'这样的日期
        一定不会查询到结果

**Response** `200` :

.. sourcecode:: json
    {
    "data":[
        {
            "class_id":1,
            "class_name":"UI设计三班",
            "sign_total_count":0,
            "stu_total_count":1
        },
        {
            "class_id":2,
            "class_name":"Python培训一班",
            "sign_total_count":1,
            "stu_total_count":2
        },
        {
            "class_id":3,
            "class_name":"PHP培训二班",
            "sign_total_count":0,
            "stu_total_count":1
        }
    ],
    "total_count":3
}

