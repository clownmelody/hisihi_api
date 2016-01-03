Herovii Api V1 (Test Version)
===============================

Api V1 说明
~~~~~~~~~~~~~~~~

互联网数据可贵，请尽量保护用户数据和服务器资源的安全。

1. 除了 `POST v1/token` 和 `POST v1/token/info` (获取令牌及查询令牌信息)外所有Api都
   需要申请令牌来调用
#. 令牌具有时效性，当令牌过期时需要使用app_key和app_secret或者账号、密码重新获取令牌
#. 令牌分为应用令牌和用户令牌，两种令牌的获取都可以通过调用 `POST v1/token`来获取
#. 不建议客户端存储用户账号、密码，而应该通过refresh_token刷新令牌
#.  不建议客户端存储App_Secret，可以存放App_Key。App_Secret应该放在App的前置服务器中
#. 数据格式统一使用json，不支持xml
#. 所有Api均支持跨域，目前不做任何限制，后期根据情况可能会限制跨域访问
#. Api遵从严格的HTTP动作并采用标准的 :ref:`Http Status Code <status>` 作为响应状态，
   建议采用HTTP状态码作为Api调用是否成功的标识
#. POST/PUT时中文使用UTF-8编码
#. Api返回的时间均为时间戳，请自行转换
#. Api同时支持HTTP和HTTPS两种协议。由于目前没有购买证书，客户端有可能会被阻止使用HTTPs
   协议，所以建议目前使用HTTP协议访问




.. toctree::
   :maxdepth: 2

   tips
   status
   enums
   token
   pk
   news
   sms
   user
   online
   mall
   file
   lecture
   statistic
   org
   student
   classmate
   blz
   feedback
   tag
   im
   imPushService

