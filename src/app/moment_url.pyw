# -*- coding: UTF-8 -*-

import urllib.request
import urllib.error
import datetime
import json
import os

BASE_URL = 'https://moment.douban.com/api/stream/date/'

class Moment:

    def __init__(self, date):
        self.date = date

    def read_json(self):
        try: self.req = urllib.request.urlopen(BASE_URL + self.date)
        except urllib.error.URLError as e:
            return False
            # print(e.reason)
        else:
            self.url = urllib.request.urlopen(BASE_URL + self.date)
            self.content = self.url.read().decode('utf-8')
            self.data = json.loads(self.content)
            if 'total' in self.data.keys():
                self.total = self.data['total']
                if 'posts' in self.data.keys():
                    self.posts = self.data['posts']
            else:
                return False
            if self.total == 0:
                return False

    def write_data(self):
        if os.path.exists('data\\' + self.date + '.json'):
            with open('data\\' + self.date + '.json', mode='r+', encoding='utf-8') as f:
                data = json.load(f)
            if data['total'] != self.total:
                with open('data\\' + self.date + '.json', mode='w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False)
        else:
            if os.path.exists('data\\') == False:
                os.mkdir('data\\')
            with open('data\\' + self.date + '.json', mode='w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_posts(self):
        return self.data

now_day = datetime.datetime.now()
yes_day = now_day + datetime.timedelta(days=-1)
# print(now)

def first_run():
    tmp = True
    i = 0
    while tmp:
        i -= 1
        pev_day = now_day + datetime.timedelta(days=i)
        if '%04d-%02d-%02d' % (pev_day.year, pev_day.month, pev_day.day) == '2014-05-12':
            run(pev_day.year, pev_day.month, pev_day.day)
            tmp = False
        else:
            run(pev_day.year, pev_day.month, pev_day.day)

def run(year, month, day):
    str_date = '%04d-%02d-%02d' % (year, month, day)
    date_moment = Moment(str_date)
    date_moment.read_json()
    date_moment.write_data()

def check():
    tmp = True
    i = 0
    path = os.path.dirname(os.path.abspath('__file__')) + '\\data'
    if os.path.exists(path):
        file_list = os.listdir(path)
        while tmp:
            i -= 1
            pev_day = now_day + datetime.timedelta(days=i)
            if '%04d-%02d-%02d.json' % (pev_day.year, pev_day.month, pev_day.day) in file_list:
                tmp = False
            elif '%04d-%02d-%02d' % (pev_day.year, pev_day.month, pev_day.day) == '2014-05-12':
                run(pev_day.year, pev_day.month, pev_day.day)
                tmp = False
            else:
                run(pev_day.year, pev_day.month, pev_day.day)
        if len(file_list) == 0:
            first_run()
    else:
        first_run()


check()
run(yes_day.year, yes_day.month, yes_day.day)
run(now_day.year, now_day.month, now_day.day)
