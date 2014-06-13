# -*- coding: UTF-8 -*-

import datetime
import json
import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
import flask

# from app import app

app = Flask(__name__)

# now_day = datetime.datetime.now()
# page_day = now_day

@app.route('/')
@app.route('/index')
def index():
    global pev_day_num
    now_day = datetime.datetime.now()
    page_day = now_day
    pev_day = now_day + datetime.timedelta(days=-1)
    pev_day_num = '%04d%02d%02d' % (pev_day.year, pev_day.month, pev_day.day)
    date = '%04d-%02d-%02d' % (page_day.year, page_day.month, page_day.day)
    path = os.path.dirname(os.path.abspath('__file__'))
    if os.path.exists(path + '/data/' + date + '.json'):
        with open(path + '/data/' + date + '.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
        total = data['total']
        posts = data['posts']
        date = data['date']
        pev_url = flask.url_for('specific_day', day_num = pev_day_num)
        return flask.render_template("index.html",
                              title = date,
                              total = total,
                              posts = posts,
                              pev_url = pev_url)
    else:
        pev_day_dete = pev_day.strftime('%Y-%m-%d')
        with open(path + '/data/' + pev_day_dete + '.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
        total = data['total']
        posts = data['posts']
        date = data['date']
        pev_pev_day = pev_day + datetime.timedelta(days=-1)
        pev_pev_day_num = pev_pev_day.strftime('%Y%m%d')
        pev_url = flask.url_for('specific_day', day_num = pev_pev_day_num)
        return flask.render_template("index.html",
                              title = date,
                              total = total,
                              posts = posts,
                              pev_url = pev_url)

@app.route('/day/<day_num>')
def specific_day(day_num):
    global pev_day_num, next_day_num
    page_day = datetime.datetime.strptime(day_num, '%Y%m%d')
    pev_day = page_day + datetime.timedelta(days=-1)
    next_day = page_day + datetime.timedelta(days=1)
    pev_day_num = pev_day.strftime('%Y%m%d')
    next_day_num = next_day.strftime('%Y%m%d')
    date = '%04d-%02d-%02d' % (page_day.year, page_day.month, page_day.day)
    path = os.path.dirname(os.path.abspath('__file__'))
    pev_url = flask.url_for('specific_day', day_num = pev_day_num)
    next_url = flask.url_for('specific_day', day_num = next_day_num)
    if day_num == datetime.datetime.now().strftime('%Y%m%d'):
        if os.path.exists(path + '/data/' + date + '.json'):
            with open(path + '/data/' + date + '.json', mode='r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            with open(path + '/data/' + pev_day.strftime('%Y-%m-%d') + '.json', mode='r', encoding='utf-8') as f:
                data = json.load(f)
        date = data['date']
        total = data['total']
        posts = data['posts']
        return flask.render_template("index.html",
                          title = date,
                          total = total,
                          posts = posts,
                          pev_url = pev_url)
    else:
        with open(path + '/data/' + date + '.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
        date = data['date']
        total = data['total']
        posts = data['posts']
        if os.path.exists(path + '/data/' + next_day.strftime('%Y-%m-%d') + '.json'):
            return flask.render_template("specificday.html",
                              title = date,
                              total = total,
                              posts = posts,
                              pev_url = pev_url,
                              next_url = next_url)
        else:
            return flask.render_template("index.html",
                          title = date,
                          total = total,
                          posts = posts,
                          pev_url = pev_url)


def today():
    global pev_day_num
    now_day = datetime.datetime.now()
    page_day = now_day
    pev_day = now_day + datetime.timedelta(days=-1)
    pev_day_num = '%04d%02d%02d' % (pev_day.year, pev_day.month, pev_day.day)
    date = '%04d-%02d-%02d' % (page_day.year, page_day.month, page_day.day)
    path = os.path.dirname(os.path.abspath('__file__'))
    if os.path.exists(path + '/data/' + date + '.json'):
        with open(path + '/data/' + date + '.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        pev_day_dete = pev_day.strftime('%Y-%m-%d')
        with open(path + '/data/' + pev_day_dete + '.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
    return data

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(debug = True)
    # pass
