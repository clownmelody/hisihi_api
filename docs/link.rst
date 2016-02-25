.. _link:

导航黄页
==========

返回导航网址列表和分类列表
~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL**::

    GET     link/yellow_pages？page=2


**Parameters** ::


* page:页码，默认值为1
* per_page:每页条数，默认值为每页20条


**Response** `200`::

{
* name：网址（分类）名称
* URL：网址链接
* iconURL：图标资源地址
* recommend:推荐标识
* initialView：初始访问量
}





返回推荐网址
~~~~~~~~~~~~~~

**URL**::

    GET     link/recommend_yellow_pages

**Parameters**::


**Response** `200`::

{
* name：网址（分类）名称
* URL：网址链接
* iconURL：图标资源地址
* recommend:推荐标识
* initialView：初始访问量
}





添加记录
~~~~~~~~~~

**URL**::

    POST     link/yellow_page

**Parameters**::

* name：网址（分类）名称
* URL：网址链接
* iconURL：图标资源地址
* recommend:推荐标识
* initialView：初始访问量
* stat:是否删除标识

**Response** `201` ::



更新/删除记录
~~~~~~~~~~~~~~

**URL**::

    PUT     link/yellow_page

**Parameters**::

* name：网址（分类）名称
* URL：网址链接
* iconURL：图标资源地址
* recommend:推荐标识
* initialView：初始访问量
* stat:是否删除标识

**Response** `202` ::
