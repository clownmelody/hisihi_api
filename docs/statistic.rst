.. _statistic:

统计
==========

活动的PV量加1次
~~~~~~~~~~~~~~~
URL::

    PUT     online/pv+1

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

    PUT     online/share+1

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

    PUT       pk/download+1

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

