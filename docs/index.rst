herovii ApiV1（测试版）
=======================

Api V1 说明
----------------

所有的API发布版本均以 **api.hisihi.com/v1/** 开头, 测试版均以
**test.api.hisihi.com/v1** 开头。例如::

    PUT /pk/download+1

你需要使用如下URL来调用::

    PUT https://api.hisihi.com/v1/pk/download+1
    PUT-Data:  {"oid" : "4", "channel" : 1 }

关于POST、PUT等HTTP动作的数据提交
------------------------------

任何参数提交（除**GET**参数外）均需要严格符合JSON数据格式。比如，以单引号表示JSON
的键或者值。在herovii api中所有json数据字符串都必须以双引号" " 来引用。

**错误的参数**::

        POST {‘oid’:'3', 'channel': 'online'}

**正确的参数**::

        POST {"oid":"3", "channel": "oneline"}


关于API调用的返回结果
----------------------

所有的调用结果均以JSON形式返回，不支持XML格式。除具体对象返回结果（如获取用户基本信息），
通用返回格式均包含msg、code及request三个参数组成的JSON响应消息::

        {
          "code": 1003,
          "msg": "token is expired",
          "request": "PUT  /v1/pk/download+1"
        }

**code**表示错误码（具体错误码可以参见错误码页）；**msg**表示错误信息；**request**表示
此次访问的HTTP地址。***错误返回码及其有用***，当错误消息未能解决你的问题时，请查找错误
返回码，以获取有效的错误消息。



.. toctree::
   :maxdepth: 2

   status

