#!/usr/bin/env python

import sys
import os.path
from flask import Flask
app = Flask(__name__)

sys.path.append(os.path.join(sys.path[0], 'lib'))
import pyrt

DEBUG=True


@app.route('/')
def hello_world():
    return 'Hello Worlds!'

@app.route('/q/<queue>')
def show_queue(queue):
    rt = pyrt.RT_Server()
    rt.login()
    condition = "Queue = '%(queue)s' AND ( Status = 'new' OR Status ='open' OR Status = 'stalled' OR Status = 'resolved' )" % locals()
    # condition = "Queue = '%(queue)s'" % locals()
    tickets = rt.tickets_where(condition)

    s = map(str, tickets)
    return "<pre>" + "\n--\n".join(s) + "</pre>"


if __name__ == '__main__':
    app.run(debug=DEBUG)
