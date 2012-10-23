#!/usr/bin/env python

import json
import sys
import os.path
from flask import Flask
app = Flask(__name__)

sys.path.append(os.path.join(sys.path[0], 'lib'))
import pyrt
import pprint

DEBUG=True


@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/q/<queue>')
def show_queue(queue):
    rt = pyrt.RT_Server()
    rt.login()
    condition = "Queue = '%(queue)s' AND ( Status = 'new' OR Status ='open' OR Status = 'stalled' OR Status = 'resolved' )" % locals()
    # condition = "Queue = '%(queue)s'" % locals()
    tickets = rt.tickets_where(condition)

    s = map(str, tickets)
    return "<pre>" + "\n--\n".join(s) + "</pre>"

@app.route('/api/v1.0/queues/<queue>.json')
def show_queue(queue):
    rt = pyrt.RT_Server()
    rt.login()
    condition = "Queue = '%(queue)s' AND ( Status = 'new' OR Status ='open' OR Status = 'stalled' OR Status = 'resolved' )" % locals()
    # condition = "Queue = '%(queue)s'" % locals()
    tickets = rt.tickets_where(condition)

    if DEBUG:
        return json.dumps(tickets, indent=4)
    else:
        return json.dumps(tickets)

@app.route('/api/v1.0/queues/<queue>/status.json')
def show_queue_by_status(queue):
    rt = pyrt.RT_Server()
    rt.login()
    condition = "Queue = '%(queue)s' AND ( Status = 'new' OR Status ='open' OR Status = 'stalled' OR Status = 'resolved' )" % locals()
    # condition = "Queue = '%(queue)s'" % locals()
    tickets = rt.tickets_where(condition)

    out = list()
    statuses = ['new','open','stalled','resolved']
    for status in statuses:
        swim_lane = dict()
        swim_lane['Name'] = status
        swim_lane['Tasks'] = [ ticket for ticket in tickets if ticket['Status'] == status ]
        out.append(swim_lane)


    if DEBUG:
        return json.dumps(out, indent=4)
    else:
        return json.dumps(out)



if __name__ == '__main__':
    app.run(debug=DEBUG)
