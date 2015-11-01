__author__ = 'bliss'

import sys
from herovii import create_app
from herovii.models import db

app = create_app({'DEBUG': True})


@app.route('/-ddd/<int:uid>')
def hello_world(uid):
    return 'Hello World!'+'   '+str(uid)

if __name__ == '__main__':
    app.run()

