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
        "teacher_group_id":5
    }

**Parameters**:

* uid：教师id
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
              "group_id": 1,
              "group_title": "用户组1",
              "teachers": [
                {
                  "nickname": "admin",
                  "sex": 0,
                  "uid": 1
                },
                {
                  "nickname": "大家好，我是雪菲菲",
                  "sex": 0,
                  "uid": 367
                }
              ]
            },
            {
              "group_id": 2,
              "group_title": "用户组2",
              "teachers": [
                {
                  "nickname": "中国合伙人",
                  "sex": 1,
                  "uid": 378
                }
              ]
            }
          ],
          "org_id": 1
     }

**Memo**：
   需要OrgAdminScope权限