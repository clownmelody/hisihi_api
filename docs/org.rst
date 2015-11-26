.. _org:

v1/org
===========
允许我偷个懒，这个类属性太多，贴段代码好了。POST、PUT参数就是属性名字。不需要传入完整属性，
需要添加、修改哪个属性就给哪个属性赋值。

.. literalinclude:: ../herovii/models/org.py

创建机构信息
~~~~~~~~~~~

**URL**::

    POST      /

**POST Sample**：

.. sourcecode:: json

    {
       "name": "我是培训机构",
       "slogan": "培训好！"
       "logo": "img_url"
    }

**Parameters**:

参数均为顶部OrgInfo类中的属性字段。"name"为必填字段，其余均为选填。
如果需要上传　** logo ** ，请先调用 :ref:`File API <file>`

**Response** `201`:

.. sourcecode:: json

    {
        'lat': '30.498029',
        'video_img': 'video_img',
        'logo': 'logo',
        'introduce': '介绍',
        'lon': '114.421816',
        'pv': 0,
        'guarantee_num': 200,
        'slogan': '培训！培训！培训万岁',
        'name': '火星时代',
        'id': 2,
        'video': 'video',
        'location': '武汉市洪山区光谷新世界1602',
        'phone_num': '0278888888',
        'advantage': '无敌#高效'
    }


更新机构信息
~~~~~~~~~~~~~~~~~~~~~~

** URL **::

    PUT        /

**PUT Sample**：

.. sourcecode:: json

    {
       "id"  : 1
       "name": "北大青鸟",
       "slogan": "培训好！"
       "logo": "img_url"
    }

**Parameters**:

参数均为顶部OrgInfo类中的属性字段。"id"为必填字段，其余均为选填。
如果需要上传　** logo ** ，请先调用 :ref:`File API <file>`


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


