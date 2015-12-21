.. _org:

机构
===========
允许我偷个懒，这个类属性太多，贴段代码好了。POST、PUT参数就是属性名字。不需要传入完整属性，
需要添加、修改哪个属性就给哪个属性赋值。

.. literalinclude:: ../herovii/models/org.py

创建机构信息
~~~~~~~~~~~

**URL**::

    POST      /org

**POST Sample**：

.. sourcecode:: json

   {
       "name": "我是培训机构",
       "slogan": "培训好！",
       "logo": "img_url",
       "uid": 555,
       "type": "1#2",
       "phone_num":"18698978786",
       "city": "武汉"
    }

**Parameters**:

参数均为顶部OrgInfo类中的属性字段。出现在示例中字段信息为必填信息。
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

**URL**::

    PUT        /org

**PUT Sample**::

    {
       "id"  : 1
       "name": "北大青鸟",
       "slogan": "培训好！"
       "logo": "img_url"
    }

**Parameters**:

参数均为顶部OrgInfo类中的属性字段。"id"为必填字段，其余均为选填。
如果需要上传　**logo** ，请先调用 :ref:`File API <file>`


查询机构信息
~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    GET      /org

**Parameters**:

* uid : 通过机构管理员id号来查找机构的基本信息
* oid : 通过机构id号来查找机构的基本信息


**Memo**:
1. 如果任何参数都不传，则会返回当前用户的机构信息
2. uid与oid为互斥参数，且oid的优先级高于uid.如果同时传递uid和oid，以oid为判断条件



