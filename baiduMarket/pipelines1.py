from scrapy.exceptions import DropItem
from scrapy import signals
from scrapy import log
from scrapy.xlib.pydispatch import dispatcher
import MySQLdb
#try:
#    from hashlib import md5
#except:
#    from md5 import md5
import hashlib
from md5 import md5
import subprocess
import time
import os
import gzip,urllib
from com_fm import *
import tool
import sys
import json
import codecs 
def safe_remove(path):
    try:
        os.remove(path)
    except Exception, e:
        e = str(e)
        print 'safe_remove except: ' + e

def sumfile(fobj):
    m = md5()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def file_md5(filename):
    try:
       f = open(filename, 'rb')
    except:
       print 'open file fail'
       return ""
    if (len(f.read()) == 0):
        f.close()
        return ""
    f.seek(0)
    md5 = sumfile(f)
    f.close()
    return md5

def wget_file(download_url, path):
    cmd = "wget -q '" + download_url + "' -O " + path
    os.system(cmd)
    os.system(cmd)
    if (os.path.exists(path)):
        filemd5 = file_md5(path)
        return filemd5
    else:
        return ""  

import shutil

class BaidumarketPipeline(object):
     def process_item(self,item,spider):
        fil=wget_file(item['download_url'],'/root/home/chenpeng/app_baidu/download/app.gz')
        print 'download url:'+item['download_url']
        print 'fil:'+fil
        content_pa=fil
        content_pa1='/root/home/chenpeng/app_baidu/download/'
        content_path=content_pa1+content_pa
        shutil.copy('/root/home/chenpeng/app_market_crawl/download/app.gz',content_path)




   
