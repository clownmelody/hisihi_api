.. _token:

v1/token
===========

获取令牌
~~~~~~~~~~~

**URL**::

    POST      /

**POST Sample**：

.. sourcecode:: json

    {
        "account":"MmyQsBlY",
        "secret":"E4Drd2Qx",
        "type":"230",
        "device":"Nokia-Lumia-920-TW"
    }

**Parameters**:

* account：用户账号或者app_key
* secret: 用户密码或者app_secret
* type: 账号类型，可取值参见 :ref:`枚举类型说明 <enums>`
* device: 设备唯一标识。目前没有进行多端登录控制，所以不需要赋值或者传递空值

**Response** `201`:

.. sourcecode:: json

    {
        "token": "eyJleHAiOjE0NDc0MjkxOTIsImlhdCI6MTQ0NzE2OTk5MiwiYWxnIjoiSFMyNTYifQ
                 .eyJzY29wZSI6Ik9ubGluZTAwMDEiLCJ1aWQiOiJNbXlLc0JsSiIsImFjX3R5cGUiOi
                 IxIn0.28Z7wog3fqXm_5V7f8is_O7kxK1c88K50gD2fk4lwmo"
    }

.. note::
    ' / '   表示v1/token 完整示例：`http://api.hisihi.com/v1/token` 后续不再赘述。此接口
    不需要Http Basic验证


[
  [
    {
      "blz_id": "2345234535",
      "confirm_time": null,
      "course_id": 76,
      "id": 2,
      "organization_id": 2,
      "phone_num": "13945670987",
      "student_name": "李二狗",
      "student_uid": 565,
      "student_university": "武汉大学"
    },
    "李长春",
    "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b11e133f0-05505543.jpg"
  ],
  [
    {
      "blz_id": "234523452345",
      "confirm_time": null,
      "course_id": 76,
      "id": 1,
      "organization_id": 2,
      "phone_num": "13876567898",
      "student_name": "赵虎",
      "student_uid": 566,
      "student_university": "武汉大学"
    },
    "皇帝的新衣",
    "http://hisihi-avator.oss-cn-qingdao.aliyuncs.com/2015-11-13/5645b325d2dd7-05505543.jpg"
  ]
]

> session.query(User).filter(text("id<:value and name=:name")).\
...     params(value=224, name='fred').order_by(User.id).one()

def view_student_count(oid, form):
    """查找status=1（正在审核的学生）和status=2已经审核过的学生数量"""
    since = form.since.data
    end = form.end.data
    page = int(form.page.data)
    per_page = int(form.per_page.data)
    start = (page-1) * per_page
    stop = start+per_page
    time_line = ''
    if since and end:
        time_line = 'create_time >=' + since + 'and create_time <=' + end
    if since and not end:
        time_line = 'create_time >=' + since
    if not since and end:
        time_line = 'create_time <=' + end
    counts = db.session.query(func.count('*')).\
        filter(Enroll.organization_id == oid, text(time_line)).\
        group_by(Enroll.status).\
        having(or_(Enroll.status == 1, Enroll.status == 2)).\
        slice(start, stop)
    return counts
