.. _status:

HTTP返回状态说明
=================
Hero API 通过HTTP Status Code来说明 API 请求是否成功 下面的表格中展示了可能的
HTTP Status Code以及其含义

========   ========================  =====================
状态码             含义                  A and B
========   ========================  =====================
200         OK                        请求成功
201         CREATED                   创建成功
202         ACCEPTED                  更新成功
400         BAD REQUEST               请求包含不支持的参数
401         UNAUTHORIZED                未授权
403         FORBIDDEN                 被禁止访问
404         NOT FOUND                 请求的资源不存在
500        INTERNAL SERVER ERROR         内部错误

========   ========================  =====================


python::

    @api.route('/download+1', methods=['PUT'])
    @auth.login_required
    def downloads_plus_1():
        """ 下载数+1, channel表示通过哪一种方式新增的下载量
        channel = online or 1 表示通过活动新增的下载量，此时PUT的Data中需要包含'oid'
        参数，表示活动号
        :PUT:
            sample: {"oid":"3", "channel":"online"}
        :Arg:
            sample: ?channel = 1 or channel = online
        :return:
        """
        form = DownloadPlus1Form().create_api_form()

        head_agent = request.user_agent.string
        mobile_race = android_ipad_iphone(head_agent)
        count = downloads_plus(form.channel.data, oid=form.oid.data, mobile_race=mobile_race)
        if count >= 1:
            return success_json(), 202
        else:
            raise UnknownError()

