# -*- coding: UTF-8 -*-

import datetime
import json
import os
from app import app
import flask

# now_day = datetime.datetime.now()
# page_day = now_day

@app.route('/')
@app.route('/index')
def index():
    data = today()
    date = data['date']
    total = data['total']
    posts = data['posts']
    # pev_day_int = today().pev_day_int
    pev_url = flask.url_for('specific_day', day_num = pev_day_num)
    return flask.render_template("index.html",
                          title = date,
                          total = total,
                          posts = posts,
                          pev_url = pev_url)

@ app.route('/day/<day_num>')
def specific_day(day_num):
    global pev_day_num, next_day_num
    page_day = datetime.datetime.strptime(day_num, '%Y%m%d')
    pev_day = page_day + datetime.timedelta(days=-1)
    next_day = page_day + datetime.timedelta(days=1)
    pev_day_num = pev_day.strftime('%Y%m%d')
    next_day_num = next_day.strftime('%Y%m%d')
    date = '%04d-%02d-%02d' % (page_day.year, page_day.month, page_day.day)
    path = os.path.dirname(os.path.abspath('__file__'))
    with open(path + '\\app\\data\\' + date + '.json', mode='r', encoding='utf-8') as f:
        data = json.load(f)
    date = data['date']
    total = data['total']
    posts = data['posts']
    pev_url = flask.url_for('specific_day', day_num = pev_day_num)
    next_url = flask.url_for('specific_day', day_num = next_day_num)
    if day_num == datetime.datetime.now().strftime('%Y%m%d'):
        return flask.render_template("index.html",
                          title = date,
                          total = total,
                          posts = posts,
                          pev_url = pev_url)
    else:
        return flask.render_template("specificday.html",
                          title = date,
                          total = total,
                          posts = posts,
                          pev_url = pev_url,
                          next_url = next_url)

def today():
    global pev_day_num
    now_day = datetime.datetime.now()
    page_day = now_day
    pev_day = now_day + datetime.timedelta(days=-1)
    pev_day_num = '%04d%02d%02d' % (pev_day.year, pev_day.month, pev_day.day)
    date = '%04d-%02d-%02d' % (page_day.year, page_day.month, page_day.day)
    path = os.path.dirname(os.path.abspath('__file__'))
    with open(path + '\\app\\data\\' + date + '.json', mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data
