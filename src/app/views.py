# -*- coding: UTF-8 -*-

import datetime
import json
import os
from app import app
import flask

now = datetime.datetime.now()

@app.route('/')
@app.route('/index')
def index():
    data = today()
    date = data['date']
    total = data['total']
    posts = data['posts']
    return flask.render_template("index.html",
                          title = date,
                          total = total,
                          posts = posts)

def today():
    date = '%04d-%02d-%02d' % (now.year, now.month, now.day)
    path = os.path.dirname(os.path.abspath('__file__'))
    with open(path + '\\app\\data\\' + date + '.json', mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data