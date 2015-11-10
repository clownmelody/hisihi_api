.. _token:

v1/token
===========

获取令牌
~~~~~~~~~~~

URL::

    POST      /

POST：

.. sourcecode:: json

    {
        "uid":"MmyQsBlY",
        "secret":"E4Drd2Qx",
        "type":"1"
    }

Parameters:

* uid：用户账号或者app_key
* secret: 用户密码或者app_secret
* type: 账号类型，目前只有App类，可取值 1, "1", 或者"App"

Response with:

.. sourcecode:: json

    {
        "token": "eyJleHAiOjE0NDc0MjkxOTIsImlhdCI6MTQ0NzE2OTk5MiwiYWxnIjoiSFMyNTYifQ
                 .eyJzY29wZSI6Ik9ubGluZTAwMDEiLCJ1aWQiOiJNbXlLc0JsSiIsImFjX3R5cGUiOi
                 IxIn0.28Z7wog3fqXm_5V7f8is_O7kxK1c88K50gD2fk4lwmo"
    }

.. note::
    ' / '   表示v1/token 完整示例：`http://api.hisihi.com/v1/token` 后续不再赘述。此接口
    不需要Http Basic验证


获取令牌信息
~~~~~~~~~~~~~~~~

URL::

    POST      /info

POST::

    {
        "token":"eyJleHAiOjE0NDc0MzQ0OD"
    }

Parameters:

* token: 令牌（不需要base64加密）

Response with::

    {
        "create_at": 1447175285,
        "expire_in": 1447434485,
        "scope": "Online0001"
    }

* create_at: token的创建时间
* expire_in: token的过期时间
* scope: token的权限域

Memo:

    此接口同样不需要Http Basic 验证


