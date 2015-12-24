.. _file:

文件
===========

上传文件
~~~~~~~~~~~

**URL**::

    POST      file/

**POST Sample**：

提交多个file类型的字段，必须在HTTP头中加入

**Parameters**:

支持多文件上传。一次请求的body里可以有多个Key：[File1,File2,File3....]键值对；而每个
键值对中的Files可以加入多个File。建议每个Key仅对应一个File。key值的设定根据客户端使用
的不同框架会有不同的设置方式。比如，在HTML5中，key值就是input控件的name属性值。

**Response** `201`:

.. sourcecode:: json

    {
        "key1": [url1,url2,url3]
        "key2": [url4]
        "key3": [url5]
    }

**Memo**:

* 一次上传的所有文件总大小不可以超过6MB，否则会返回一个413错误码
* 支持以下文件类型['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'amr']
* 如果任何一个文件上传失败都会返回错误码，并不会返回哪个文件上传成功，哪些文件上传失败
  如果有这样的需求，请联系leilei

关于文件上传后的后续处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~

当文件上传成功后，服务器将返回所有上传文件的URI。这个URI是一个文件的完全访问地址。
通常来说每个文件URI都会在你后续的API调用中使用到，因为文件的上传仅仅是在网络上给这个
文件一个资源位置，并没有和当前的用户对象有任何的直接关联。

一个栗子：创建用户时可能需要上传头像。那么完整的用户创建应该分为两步，上传头像文件取得
文件的URL；将URL加入到用户基本信息里，再提交到服务器。

所有涉及到文件的操作都应该遵循这个原则，不要上传文件后不做后续操作，白白浪费服务器资源


关于CDN加速和图片裁剪、缩放
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

服务器目前返回的文件URI是经过CDN加速的URI。原始URI不再开放。通过CDN加速的URI支持对
图片文件进行裁剪和缩放。例如：

http://pic.hisihi.com/2015-11-22%2F1448124241200305.jpg@300w

使用 `@300w` 调用这个URI将对 *1448124241200305.jpg* 裁剪，得到一张定宽（300），保持比例的新图片
更多的裁剪、缩放、管道示例参见：

http://help.aliyun.com/document_detail/oss/oss-img-api/image-processing/resize.html


机构上传图片
~~~~~~~~~~~~~~~~~

**URL**::

    POST      org/<int:oid>/pics

**POST Sample**：

.. sourcecode:: json
    [
        {
            "url" : "http://pic.hisihi.com",
            "description" : "测试图片"
            "type": 1
            "organization_id" : 2
        }
    ]

**Parameters**:

* url：图片路径，调用图片上传接口获取
* description: 描述信息
* type: 图片用途; 1 学生作品  2 机构环境
* organization_id: 机构id号

**Response** `201`:

.. sourcecode:: json

    [
        {
            "id" ：2
            "url" : "http://pic.hisihi.com",
            "description" : "测试图片"
            "type": 1
            "organization_id" : 2
        }
    ]

**Memo** :
   需要OrgAdminScope权限.支持一次上传多张图片信息


获取机构图片
~~~~~~~~~~~~~~~~~~~~~

**URL**::

    GET      org/<int:oid>/pics?type=:type&page=:page&per_page=:per_page

**Parameters**:

* oid：机构id号
* type: 图片用途; 0 全部 , 1 学生作品  2 机构环境(可选，默认是0)
* page,per_page 分页

**Response** `201`:

.. sourcecode:: json

    {
      [
        {
          "description": "放飞梦想-",
          "id": 18,
          "organization_id": 2,
          "type": 1,
          "url": "http://pic.hisihi.com/2015-12-02/565dcbd5049cb.jpg"
        },
        {
          "description": "VIP卡1",
          "id": 17,
          "organization_id": 2,
          "type": 1,
          "url": "http://pic.hisihi.com/2015-12-02/565dcb467f114.jpg"
        },
        {
          "description": "花好月圆",
          "id": 16,
          "organization_id": 2,
          "type": 1,
          "url": "http://pic.hisihi.com/2015-11-12/56440a5ccd24e.jpg"
        },
        {
          "description": "抗战胜利海报",
          "id": 15,
          "organization_id": 2,
          "type": 1,
          "url": "http://pic.hisihi.com/2015-12-02/565dcb1f89843.jpg"
        }
      ],
      "total_count": 16
    }

获取每日签到二维码
~~~~~~~~~~~~~~~~~~~~

**URL**::

    POST        org/<int:oid>/qrcode/sign-in/today


**Parameters**:

* oid：机构id号

**Response** `201`:

.. sourcecode:: json

    [
        {
            "id" ：2
            "qrcode_url" : "v1/1/student/0/sign-in/2015-12-03",
            "date" : "2015-12-3"
            "organization_id": 1
            "oss_url" : "http://pic.hisihi.com/2015-2-3/23942374294.jpg"
        }
    ]

**Memo**:

oss_url 是二维码图片的资源地址。qrcode_url是二维码指向的访问地址。通常用户需要
对扫描出的二维码路径做进一步的处理。处理项目包括：

1. 在qrcode_url前面加上Host地址，如http://dev.api.hisihi.com或者http://api.hisihi.com
#. 将qrcode_url的student/0/中的0替换为需要签到的用户的id号


获取二维码（通用）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    POST        file/qrcode

**POST Sample**：

.. sourcecode:: json

    {
        "url": "http://sina.com"
    }

**Parameters**:

* url: 需要嵌入到二维码中的Url路径或者其他信息


**Response** `201`:

.. sourcecode:: json

    {
        'qrcode_url': "http://pic.hisihi.com/2015-2-3/23942374294.png"
    }

qrcode_url 生成二维码的路径
