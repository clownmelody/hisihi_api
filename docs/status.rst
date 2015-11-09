HTTP返回状态说明
=================
Hero API 通过HTTP Status Code来说明 API 请求是否成功 下面的表格中展示了可能的
HTTP Status Code以及其含义

=======  =====================  =====================
状态码             含义              A and B
=======  =====================  =====================
200          OK                      请求成功
201         CREATED                  创建成功
202        ACCEPTED                  更新成功
400       BAD REQUEST             请求包含不支持的参数
401       UNAUTHORIZED                未授权
403        FORBIDDEN                 被禁止访问
404       NOT FOUND                请求的资源不存在
500    INTERNAL SERVER ERROR         内部错误

=======  =====================  =====================