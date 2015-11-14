.. _enums:

枚举变量
============

AccountTypeEnum 账号类型枚举
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    class AccountTypeEnum(Enum):
        app = 100
        user_csu_mobile = 200
        user_csu_wechat = 201
        user_csu_weibo = 202
        user_csu_qq = 203
        use_csu_social = 230
        user_org_mobile = 300

`100` 开头的表示第三方应用类注册账号，如HiSiHi Android App

* 100 : 第三方应用账号

`200` 开头的表示消费用户的账号类型

* 200 : 通过手机注册的账号
* 201 : 通过微信登陆的账号
* 202 : 通过微博登陆的账号
* 203 : 通过QQ登陆账号
* 230 : 第三方登陆账号

`300` 开头的表示机构用户的账号类型

* 300 : 通过手机注册账号