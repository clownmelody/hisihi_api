.. _online:

v1/online
==========
   online代表活动的相关资源



活动的PV量加1次
~~~~~~~~~~~~~~~
URL::

    PUT     /pv+1

PUT::

    {
        "oid": 4
    }

Parameters:
* oid: 活动的id号

Response Status `202` ::

    {
        "code": 0,
        "msg": "ok",
        "request": "PUT  /v1/online/pv+1"
    }


活动的分享次数+1
~~~~~~~~~~~~~~~
URL::

    PUT     /share+1

PUT::

    {
        "oid": 4
    }

Parameters:
* oid: 活动的id号

Response Status `202` ::

    {
        "code": 0,
        "msg": "ok",
        "request": "PUT  /v1/pk/share+1"
    }