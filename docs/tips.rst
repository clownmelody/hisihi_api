友情提示
=======================

Url 前缀
-----------------------

所有的API发布版本均以 **api.hisihi.com/v1** 开头, 测试版均以
**test.api.hisihi.com/v1** 开头。例如::

    PUT /pk/download+1

你需要使用如下URL来调用::

    PUT  https://api.hisihi.com/v1/pk/download+1
    PUT-Data:  {"oid" : "4", "channel" : 1 }


如何使用令牌访问Api?
-----------------------

目前所有Api的调用均需要使用令牌。如何获取令牌请参考 :ref:`Token <token>`。当获
取令牌后需要将token加入到Http的Header里::

    Authorization  basic eyJleHAiOjE0NDc0MjkxOTIsImlhdCI6MTQ0NzE2OTk5MiwiY
                         WxnIjoiSFMyNTYifQ.eyJzY29wZSI6Ik9ubGluZTAwMDEiLCJ
                         1aWQiOiJNbXlLc0JsSiIsImFjX3R5cGUiOiIxIn0.28Z7wog3
                         fqXm_5V7f8is_O7kxK1c88K50gD2fk4lwmo:

`Authorization` 是 **key**，后面的是 **value**。注意后面的 **:**  注意后面的
**:**  注意后面的 **:**  ......重要的事情任需要说+10086遍。（原因是Api采用的
是HttpBasic验证）以上的http发送后你会收到一个 *非法的token错误* 。原因是，你
还需要将 *value* 部分使用base64编码后再发送:

.. sourcecode:: http

    GET /v1/test/client-ip HTTP/1.1
    HOST: api.hisihi.com
    Accept: application/json; version 1
    Authorization  basic ZXlKbGVIQWlPakUwTkRjME1qa3hPVElzSW1saGRDSTZNVFEwTnp
    FMk9UazVNaXdpWVd4bklqb2lTRk15TlRZaWZRLmV5SnpZMjl3WlNJNklrOXViR2x1WlRBd01
    ERWlMQ0oxYVdRaU9pSk5iWGxMYzBKc1NpSXNJbUZqWDNSNWNHVWlPaUl4SW4wLjI4Wjd3b2c
    zZnFYbV81VjdmOGlzX083a3hLMWM4OEs1MGdEMmZrNGx3bW8=


关于POST、PUT等HTTP动作的数据提交
------------------------------

任何参数提交（除**GET**参数外）均需要严格符合JSON数据格式。不要以单引号表示JSON
的键或者值。在herovii api中所有json数据字符串都必须以双引号" " 来引用。

*错误的参数* ::

        POST {'oid':'3', 'channel': 'online'}

*正确的参数*::

        POST {"oid":"3", "channel": "oneline"}

HTTP/HTTPS Header
------------------------------
Api不会要求每次HTTP/HTTPS请求都在HTTP Header里附带 Content-type: application/json。
但是，如果你对你所使用的HTTP请求框架不熟悉的话，还是建议在HTTP头里加上Content-Type：
application/json.


关于API调用的返回结果
----------------------
所有HTTP请求只有2种类型的json返回结果:
1. 返回资源的特定信息（如获取用户基本信息）
2. 返回一组消息，指明调用是否成功。这类消息通常具有共同的消息体
通用返回格式均包含msg、code及request三个参数组成的JSON响应消息::

        {
          "code": 1003,
          "msg": "token is expired",
          "request": "PUT  /v1/pk/download+1"
        }

**code** 表示错误码（错误码详情可以参见 :ref:`Htttp Status COde<status>` ）；**msg**
表示错误信息； **request** 表示此次访问的HTTP地址。当错误消息未能解决你的问题时，请查找
错误返回码，以获取有效的错误消息。


