# -*- coding: UTF-8 -*-

import urllib.request
import urllib.error
import threading
import datetime
import sched
import time
import json
import os

BASE_URL = 'https://moment.douban.com/api/stream/date/'

##########################
#初始化sched模块的scheduler类
##########################
s = sched.scheduler(time.time,time.sleep)

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
                return True
        else:
            if os.path.exists('data\\') == False:
                os.mkdir('data\\')
            with open('data\\' + self.date + '.json', mode='w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        return False


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
            update(pev_day.year, pev_day.month, pev_day.day)
            tmp = False
        else:
            update(pev_day.year, pev_day.month, pev_day.day)

def update(year, month, day):
    run_result = ''
    str_date = '%04d-%02d-%02d' % (year, month, day)
    date_moment = Moment(str_date)
    date_moment.read_json()
    update = date_moment.write_data()
    if update:
        run_result = 'UPDATED'
    else:
        run_result = 'NONUPDATE'

    start = time.time()
    log_str = 'UDATE:' + time.ctime(start) + ' ' + run_result + '\n'
    print(log_str)
    path = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    with open(path + '\\tmp\\' + 'Log.txt', mode='ab') as f:
        f.write(log_str.encode())

def check():
    tmp = True
    i = 0
    run_result = ''
    path = os.path.dirname(os.path.abspath('__file__')) + '\\data'
    if os.path.exists(path):
        file_list = os.listdir(path)
        while tmp:
            i -= 1
            pev_day = now_day + datetime.timedelta(days=i)
            if '%04d-%02d-%02d.json' % (pev_day.year, pev_day.month, pev_day.day) in file_list:
                tmp = False
                run_result = 'NONE'
            elif '%04d-%02d-%02d' % (pev_day.year, pev_day.month, pev_day.day) == '2014-05-12':
                update(pev_day.year, pev_day.month, pev_day.day)
                tmp = False
            else:
                update(pev_day.year, pev_day.month, pev_day.day)
                run_result = 'PEV'
        if len(file_list) == 0:
            first_run()
            run_result = 'FIEST'
    else:
        first_run()
        run_result = 'FIEST'

    start = time.time()
    log_str = 'CHECK:' + time.ctime(start) + ' ' + run_result + '\n'
    print(log_str)
    path = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    with open(path + '\\tmp\\' + 'Log.txt', mode='ab') as f:
        f.write(log_str.encode())

###############################################################
#定义执行函数，并通过enter函数加入调度事件
#enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）,
#被调用触发的函数，给他的参数（注意：一定要以tuple给如，如果只有一个参数就(xx,)）
###############################################################

def perform(inc):
    """
	实现60s周期执行任务
	"""
    global now_day, yes_day
    now_day = datetime.datetime.now()
    yes_day = now_day + datetime.timedelta(days=-1)
    s.enter(inc,0,perform,(inc,))

    update(yes_day.year, yes_day.month, yes_day.day)
    update(now_day.year, now_day.month, now_day.day)


#######################
#主函数入口
#######################
def mymain(inc=1800):
    """
    入口主函数
    """
    path = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    start = time.time()
    log_str = 'START:' + time.ctime(start) + '\n'
    print(log_str)
    with open(path + '\\tmp\\' + 'Log.txt', mode='ab') as f:
        f.write(log_str.encode())
    #设置调度
    e1 = s.enter(2,1,perform,(inc,))                        # 调度设置
    e2 = s.enter(0,1,check,())
    # e3 = s.enterabs(start+5,2,perform,(inc,'first',start))              #设置调度优先级，enterabs()保证同时性
    # e4 = s.enterabs(start+5,1,perform,(inc,'second',start))
    #启动线程
    t = threading.Thread(target=s.run)    #通过构造函数例化线程
    t.start()                                                               #线程启动
    # s.cancel(e2)                                                            #取消任务调度e2
    t.join()                                                                #阻塞线程

#########################
#测试代码
if __name__ == "__main__":
    mymain()
