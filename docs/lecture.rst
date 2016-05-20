.. _lecture:

讲师
===========

创建讲师分组
~~~~~~~~~~~

**URL**::

    POST      org/lecture/group

**POST Sample**：

.. sourcecode:: json

    {
        "organization_id":"3",
        "title":"设计UI组"
    }

**Parameters**:

* organization_id：分组所属机构的ID
* title: 分组名称

**Response** `201`:

.. sourcecode:: json

    {
        "id": "3",
        "organization_id": "3",
        "title": "UI设计组"
    }

**Memo** `201`:
   需要OrgAdminScope权限


删除讲师分组
~~~~~~~~~~~~~~~~~
**URL**::

    DELETE      org/lecture/group/<int:gid>

**Parameters**:

* gid：分组id，必须为正整数

**Response** `201`:

.. sourcecode:: json

    {
        "code": 0,
        "msg": "ok",
        "request": "v1/lecture/group/2"
    }

**Memo** `201`:
   需要OrgAdminScope权限


将讲师加入某分组
~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    POST      org/lecture/group/join

**POST Sample**：

.. sourcecode:: json

    {
        "uid":3,(必填)
        "oid":2,(必填)
        "teacher_group_id":5,(必填)
        "teacher_good_at_subjects":"擅长UI设计",
        "teacher_introduce":"这个老师很帅"
    }

**Parameters**:

* uid：教师id
* oid：机构id
* teacher_group_id: 教师分组id
* teacher_good_at_subjects：老师擅长课程
* teacher_introduce: 老师简介

**Response** `201`:

.. sourcecode:: json

    {
        "id": 3,
        "uid": 3,
        "teacher_group_id": 5,
        "teacher_good_at_subjects":"擅长UI设计",
        "teacher_introduce":"这个老师很帅"
    }

**Memo** `201`:
   需要OrgAdminScope权限


将讲师加入多个分组
~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    POST      org/lecture/group/join

**POST Sample**：

.. sourcecode:: json
    [
        {
            "uid":3,(必填)
            "oid":2,(必填)
            "teacher_group_id":5,(必填)
            "teacher_good_at_subjects":"擅长UI设计",
            "teacher_introduce":"这个老师很帅"
        }
    ]

**Parameters**:

* uid：教师id
* oid：机构id
* teacher_group_id: 教师分组id
* teacher_good_at_subjects：老师擅长课程
* teacher_introduce: 老师简介

**Response** `201`:

.. sourcecode:: json

    [
      {
        "id": 156,
        "teacher_good_at_subjects": "擅长UI设计",
        "teacher_group_id": 6,
        "teacher_introduce": "这个老师很帅",
        "uid": 592
      }
    ]

**Memo** `201`:
   需要OrgAdminScope权限



讲师退出分组
~~~~~~~~~~~~~~~~~~~

**URL**:
  DELETE      org/lecture/<int:uid>/group/<int:gid>/quite

**Parameters**:

* uid：教师id
* teacher_group_id: 教师分组id

**Response** `201`:

.. sourcecode:: json

    {
        "code": 0,
        "msg": "ok",
        "request": "v1/lecture/3/group/2/quite"
    }

**Memo** `201`:
   需要OrgAdminScope权限


获取机构下所有讲师（按分组）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**:
  GET      org/<int:oid>/group/lectures

**Parameters**:

* oid：机构id号

**Response** `200`:

.. sourcecode:: json

    {
      "groups": [
        {
          "group_id": 77,
          "group_title": "平面设计分组",
          "lectures": [
            {
              "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-18/564c56eae6754-05505543.jpg",
              "lecture": {
                "nickname": "洁洁",
                "sex": 2,
                "uid": 578
              },
              "teacher_good_at_subjects": null,
              "teacher_introduce": null
            },
            {
              "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-07-17/55a8aef4d0f65-05505543.jpg",
              "lecture": {
                "nickname": "皮卡Q",
                "sex": 1,
                "uid": 103
              },
              "teacher_good_at_subjects": null,
              "teacher_introduce": null
            },
            {
              "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2016-04-21/5718976639ee3-05505543.jpg",
              "lecture": {
                "nickname": "少雷",
                "sex": 1,
                "uid": 577
              },
              "teacher_good_at_subjects": "hahhah",
              "teacher_introduce": "henhao henhao"
            }
          ]
        },
        {
          "group_id": 78,
          "group_title": "ddd",
          "lectures": []
        }
      ],
      "org_id": 41
    }

**Memo**：
   需要OrgAdminScope权限


获取机构下所有讲师（不按分组）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    GET  org/<int:oid>/lectures

**Parameters**:

* oid：机构id号
* page：页码，默认值为1
* per_page: 每页条数，默认值为每页20条

**Response** `200`::

    {
      "data": [
        {
          "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-18/564c56eae6754-05505543.jpg",
          "nickname": "洁洁",
          "teacher_good_at_subjects": null,
          "teacher_group_id": 77,
          "teacher_introduce": null,
          "uid": 578
        },
        {
          "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-07-17/55a8aef4d0f65-05505543.jpg",
          "nickname": "皮卡Q",
          "teacher_good_at_subjects": null,
          "teacher_group_id": 77,
          "teacher_introduce": null,
          "uid": 103
        },
        {
          "avatar": "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2016-04-21/5718976639ee3-05505543.jpg",
          "nickname": "少雷",
          "teacher_good_at_subjects": "hahhah",
          "teacher_group_id": 77,
          "teacher_introduce": "henhao henhao",
          "uid": 577
        }
      ],
      "total_count": 3
    }

-- end


修改老师的信息
~~~~~~~~~~~~~~~~~~~~~

**URL**::

    PUT  org/lecture/info/update

**Parameters**:（json）

* oid：机构id号(必填)
* uid：老师uid(必填)
* teacher_group_id: 老师分组id(必填)
* teacher_good_at_subjects：老师擅长课程
* teacher_introduce: 老师简介

**Response** `202`::

    {
      "id": 142,
      "teacher_good_at_subjects": "擅长ps",
      "teacher_group_id": "77",
      "teacher_introduce": "这是一个好老师",
      "uid": "577"
    }

-- end
