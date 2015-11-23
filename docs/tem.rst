.. _token:

v1/token
===========

获取令牌
~~~~~~~~~~~

**URL**::

    POST      /

**POST Sample**：

.. sourcecode:: json

    {
        "account":"MmyQsBlY",
        "secret":"E4Drd2Qx",
        "type":"230",
        "device":"Nokia-Lumia-920-TW"
    }

**Parameters**:

* account：用户账号或者app_key
* secret: 用户密码或者app_secret
* type: 账号类型，可取值参见 :ref:`枚举类型说明 <enums>`
* device: 设备唯一标识。目前没有进行多端登录控制，所以不需要赋值或者传递空值

**Response** `201`:

.. sourcecode:: json

    {
        "token": "eyJleHAiOjE0NDc0MjkxOTIsImlhdCI6MTQ0NzE2OTk5MiwiYWxnIjoiSFMyNTYifQ
                 .eyJzY29wZSI6Ik9ubGluZTAwMDEiLCJ1aWQiOiJNbXlLc0JsSiIsImFjX3R5cGUiOi
                 IxIn0.28Z7wog3fqXm_5V7f8is_O7kxK1c88K50gD2fk4lwmo"
    }

.. note::
    ' / '   表示v1/token 完整示例：`http://api.hisihi.com/v1/token` 后续不再赘述。此接口
    不需要Http Basic验证
