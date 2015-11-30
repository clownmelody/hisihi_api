.. _user:

用户
=============

创建机构管理员
~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    POST      /org/admin

**POST Sample**：

.. sourcecode:: json

    {
        "mobile": "18677771949",
        "sms_code": "567663",
        "password": "hiyouth"
    }

**Parameters**:

* mobile：手机号（注册账号）
* sms_code: 短信验证码（需要开发者首先调用 :ref:`短信发送` <sms>`
* password: 用户密码

**Response** `201`:

.. sourcecode:: json

    {
        "id": 3,
        "username": "网易"
        "mobile": "18698768787"
        'create_time": "1456878787"
    }


重置机构管理员密码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    PUT     org/admin/password

**PUT Sample**:

.. sourcecode:: json

    {
        "mobile": "18677771949",
        "sms_code": "567663",
        "password": "hiyouth",
        "type": "230"
    }

**Parameters**:

* mobile：手机号（注册账号）
* sms_code: 短信验证码（需要开发者首先调用 :ref:`短信发送` <sms>`
* password: 用户新密码
* type: 账号类型，可取值参见 :ref:`枚举类型说明 <enums>`

**Response Sample** `202`:

.. sourcecode:: json

    {
        "code": 0,
        "msg": "ok",
        "request": "PUT v1/org/admin/password"
    }


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