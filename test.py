

import base64

s = b'我是字符串'
a = base64.b64encode(s)
b = base64.b64decode(a)

print(a)
print(b)