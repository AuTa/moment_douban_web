# -*- coding: UTF-8 -*-

import urllib.request
import json

BASE_URL = 'https://moment.douban.com/api/stream/date/'

class Moment:

    def __init__(self, date):
        self.date = date

    def read_json(self):
        self.url = urllib.request.urlopen(BASE_URL + self.date)
        self.content = self.url.read().decode('utf-8')
        self.data = json.loads(self.content)
        self.total = self.data['total']
        self.posts = self.data['posts']

    def write_data(self):
        

    def get_posts(self):
        return self.posts

today = Moment('2014-06-10')
today.read_json()
print(today.posts)