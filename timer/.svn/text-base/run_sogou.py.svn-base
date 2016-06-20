#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import os
import commands

market = 'sogou'

def shouldRestart():

    f = open('/root/chenyi/baiduMarket/timer/log/cron_' + market + '.log')
    s = f.read()
    if len(s) > 841:
        f.seek(-841, 2)
        s = f.read()

        cnt = 0
        i = 0
        while True == True:
            pos = s.find('crawl running', i)
            if (pos != -1):
                cnt = cnt + 1
                i = pos + 14
            else:
                break
        if cnt >= 30:
            return True
    return False


def restart():
    
    old_path = os.getcwd()
    os.chdir('/root/chenyi/baiduMarket/timer/')

    cmd = '/usr/local/bin/scrapy crawl ' + market
    os.system(cmd)

    os.chdir(old_path)


def killProcess():

    cmd = 'ps aux | grep "/usr/bin/python /usr/local/bin/scrapy crawl ' + market + '"'
    status, output = commands.getstatusoutput(cmd)

    tmp = output.split('\n')
    for i in tmp:
        if i.find('grep') == -1 and i.find('sh') == -1:
            print i
            tmp = i.split(' ')
            l = len(tmp)
            for i in range(1, l):
                if (tmp[i] != ""):
                    pid = tmp[i]
                    break
            break

    cmd = 'kill -9 ' + pid
    status, output = commands.getstatusoutput(cmd)


cmd = 'ps aux | grep "scrapy crawl ' + market + '"'
status, output = commands.getstatusoutput(cmd)
if status == 0:
    if output.find('/usr/local/bin/scrapy crawl ' + market) == -1:
        print 'crawl stopped'
        restart()
    else:
        print 'crawl running'
        if shouldRestart() == True:
            killProcess()
            restart()
