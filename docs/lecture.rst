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
        "uid":3,
        "oid":2,
        "teacher_group_id":5
    }

**Parameters**:

* uid：教师id
* oid：机构id
* teacher_group_id: 教师分组id

**Response** `201`:

.. sourcecode:: json

    {
        "id": 3,
        "uid": 3,
        "teacher_group_id": 5
    }

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
          "group_id": 5,
          "group_title": "平面设计培训组",
          "lectures": [
            {
              "avatar": "2015-07-15/55a6367000dd5-05505543.jpg",
              "lecture": {
                "nickname": "Mouri",
                "sex": 0,
                "uid": 536
              }
            },
            {
              "avatar": "2015-07-15/55a63ecfafbfb-05505543.jpg",
              "lecture": {
                "nickname": "Use",
                "sex": 0,
                "uid": 543
              }
            }
          ]
        },
        {
          "group_id": 6,
          "group_title": "UI设计培训组",
          "lectures": [
            {
              "avatar": "2015-07-15/55a63dec7e9f8-05505543.jpg",
              "lecture": {
                "nickname": "Frankie",
                "sex": 0,
                "uid": 542
              }
            }
          ]
        },
        {
          "group_id": 7,
          "group_title": "网页设计培训组",
          "lectures": [
            {
              "avatar": "2015-07-20/55ac659074d27.png",
              "lecture": {
                "nickname": "Rfly",
                "sex": 1,
                "uid": 69
              }
            }
          ]
        }
      ],
      "org_id": 2
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
        "data":[
            {
                "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-07-15/55a62d15b9fc4-05505543.jpg",
                "nickname":"LEE",
                "teacher_group_id":5,
                "uid":529
            },
            {
                "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-07-15/55a63ecfafbfb-05505543.jpg",
                "nickname":"Use",
                "teacher_group_id":7,
                "uid":543
            },
            {
                "avatar":"http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-03-26/551369fe8358c-05505543.jpg",
                "nickname":"Rfly",
                "teacher_group_id":7,
                "uid":69
            }
        ],
        "total_count":3
    }

-- end
